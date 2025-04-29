from wheel.metadata import _

from odoo import models, fields, api
from datetime import datetime, date, timedelta

from odoo.exceptions import UserError, ValidationError

AGE_CATEGORY = [('Senior_Citizen', 'Senior Citizen'),
                ('Adult', 'Adult'),
                ('Minor', 'Minor'),
                ('Child', 'Child')]

GUARDIAN_TYPE = [('parent', 'Parent'),
                 ('sibling', 'Sibling'),
                 ('relative', 'Relative'),
                 ('friend', 'Friend'),
                 ('other', 'Other')]


class Appointment(models.Model):
    _name = "hms.appointment"
    _description = "Appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Appointment ID", copy=False, readonly=True, index=True, default="New")
    patient_id = fields.Many2one("res.patient", string="Name", required=True, tracking=True)
    # tracking = 'True'
    appointment_date = fields.Date(string="Date", required=True, default=date.today())
    appointment_reason = fields.Text(string="Reason")
    state = fields.Selection([('draft', 'Draft'),
                              ('confirm', 'Confirm'),
                              ('waiting', 'Waiting'),
                              ('in_consultation', 'In Consultation'),
                              ('done', 'Done'),
                              ('cancel', 'Cancel')],
                             string="Status", default='draft', tracking=True)
    age_category = fields.Selection(AGE_CATEGORY, string="Patient Category")
    guardian_type = fields.Selection(GUARDIAN_TYPE, string="Guardian")
    guardian_id = fields.Many2one("res.partner", string="Guardian Name")
    consultation_start = fields.Datetime(string="Consultation Start Time")
    consultation_end = fields.Datetime(string="Consultation End Time")
    consultation_time = fields.Float(string="Consultation Time")
    draft_state_start_time = fields.Datetime(string="Draft state start time")
    # draft_state_time = fields.Float(string="Draft state time")
    service_product_id = fields.Many2one("product.product", string="Products", domain=[('type', '=', 'service')])

    @api.model_create_multi
    def create(self, val_list):
        res = super(Appointment, self).create(val_list)
        for record in res:
            record.name = self.env["ir.sequence"].next_by_code('hms.appointment')
        return res

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        if self.patient_id:
            self.guardian_type = self.patient_id.guardian_type
            self.age_category = self.patient_id.age_category
            self.guardian_id = self.patient_id.guardian_id.name
            self.draft_state_start_time = datetime.now()

    @api.constrains('appointment_date')
    def appointment_date_validation(self):
        for rec in self:
            # diff = self.appointment_date - rec.appointment_date
            domain = [('patient_id', '=', rec.patient_id.id), ('appointment_date', '=', rec.appointment_date)]
            count = self.env['hms.appointment'].search_count(domain)
            if count > 1:
                raise ValidationError("You have already booked appointment this day!")

    @api.constrains('appointment_date')
    def validate_appointment_date(self):
        if self.appointment_date < date.today():
            raise UserError("Appointment date should be current date or further date!")

    def action_confirm(self):
        self.state = 'confirm'
        self.ensure_one()
        message = _("appointment confirmed")
        self.message_post(body=message)

    def action_waiting(self):
        self.state = 'waiting'

    def action_in_consultation(self):
        self.state = 'in_consultation'
        self.consultation_start = datetime.now()

    def action_done(self):
        self.state = 'done'
        self.consultation_end = datetime.now()
        diff = self.consultation_end - self.consultation_start
        total_seconds = diff.total_seconds()
        self.consultation_time = total_seconds / 60

    def _weekly_report_generator(self):
        result = {}
        today = date.today()
        start_of_week = today - timedelta(days=today.isoweekday() % 7)
        end_of_week = start_of_week + timedelta(weeks=1)

        appointments = self.env["hms.appointment"].search([
            ('appointment_date', '>=', start_of_week),
            ('appointment_date', '<', end_of_week),
        ])

        patient_name = []
        total_appointment = len(appointments)
        total_consultation_time = 0
        for patient in appointments:
            total_consultation_time += patient.consultation_time
            if patient.consultation_time > 60:
                patient_name.append(patient.patient_id.name)

        total_time_in_hours = f'{round(total_consultation_time / 60, 2)} Hours'
        result.update({'total_appointment': total_appointment, 'Total consultation time': total_time_in_hours,
                       'Patients': patient_name})
        print(result)

    def find_draft_state_time(self):
        diff = datetime.now() - self.draft_state_start_time
        total_hours = int(diff.total_seconds() / 3600)
        return total_hours

    def _auto_cancel_draft_appointment(self):
        # print("i am in _auto_cancel_draft_appointment method")
        appointments = self.env['hms.appointment'].search([('state', '=', 'draft')])

        for appointment in appointments:
            draft_time = appointment.find_draft_state_time()
            if draft_time > 24:
                appointment.state = 'cancel'

    def _weekly_cancelled_appointment_report(self):
        weekly_cancelled_appointment = []
        today = date.today()
        start_of_week = today - timedelta(days=7)
        # end_of_week = start_of_week + timedelta(weeks=1)
        end_of_week = today

        appointments = self.env["hms.appointment"].search([
            ('appointment_date', '>=', start_of_week),
            ('appointment_date', '<', end_of_week),
            ('state', '=', 'cancel')
        ])

        for appointment in appointments:
            cancelled_appointment_data = {}
            appointment_date = appointment.appointment_date
            cancelled_appointment_data.update({'Appointment number': appointment.name,
                                               'Patient name': appointment.patient_id.name,
                                               'Date of appointment': appointment_date.date()
                                               })
            weekly_cancelled_appointment.append(cancelled_appointment_data)
        # print(weekly_cancelled_appointment)

    def action_date_practice_wizard(self):
        view_id = self.env.ref('bista_hms.date_practice_wizard_form').id

        return {
            'name': 'Starting Date',
            'view_mode': 'form',
            'res_model': 'date.practice.wizard',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    def get_next_day_appointment_data(self):
        next_day_date = date.today() + timedelta(days=1)

        appointments = self.env["hms.appointment"].search([
            ('state', '=', 'confirm'),
            ('appointment_date', '=', next_day_date),
        ])
        return appointments

    def _action_send_appointment_schedule_mail_to_admin(self):
        """
        Send next day's scheduled appointment to admin.
        """
        template_id = self.env.ref('bista_hms.email_template_next_day_appointment_mail')
        template_id.send_mail(self.id, force_send=True)

    def action_send_appointment_mail(self):
        template_id = self.env.ref('bista_hms.email_template_appointment_confirmation')
        template_id.send_mail(self.id, force_send=True)
