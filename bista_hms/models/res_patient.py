from dateutil.relativedelta import relativedelta
from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from datetime import date, timedelta, datetime

BLOOD_GROUP = [('A+', 'A+ve'),
               ('B+', 'B+ve'),
               ('O+', 'O+ve'),
               ('AB+', 'AB+ve'),
               ('A-', 'A-ve'),
               ('B-', 'B-ve'),
               ('O-', 'O-ve'),
               ('AB-', 'AB-ve')]

AGE_CATEGORY = [('Senior_Citizen', 'Senior Citizen'),
                ('Adult', 'Adult'),
                ('Minor', 'Minor'),
                ('Child', 'Child')]

GUARDIAN_TYPE = [('parent', 'Parent'),
                 ('sibling', 'Sibling'),
                 ('relative', 'Relative'),
                 ('friend', 'Friend'),
                 ('other', 'Other')]


class ResPatient(models.Model):
    _name = "res.patient"
    _description = "Patient Model"

    name = fields.Char(string="Name", required=True, store=True)
    patient_code = fields.Char(string="Patient ID", default="New")
    blood_group = fields.Selection(BLOOD_GROUP, string="Blood Group", required=True)
    date_of_birth = fields.Date(string="DOB", required=True)
    age = fields.Char(string="Age")
    previous_diseases = fields.Text(string="Previous Diseases")
    phone = fields.Char(string="Phone", required=True, store=True)
    email = fields.Char(string="Email", store=True)
    mobile = fields.Char(string="Mobile", store=True)
    age_category = fields.Selection(AGE_CATEGORY, string="Patient Category")
    guardian_type = fields.Selection(GUARDIAN_TYPE, string="Guardian")
    guardian_id = fields.Many2one("res.partner", string="Guardian Name")
    patient_ids = fields.One2many("hms.appointment", "patient_id", string="Patient Appointments")
    appointment_count = fields.Integer(default=0, compute="_action_appointment_count")
    prescription_count = fields.Integer(default=0, compute="_action_prescription_count")
    weekly_visit = fields.Boolean(string="Weekly visit")
    weekly_visit_default_val = fields.Boolean(default=True)
    partner_id = fields.Many2one("res.partner", string="Partner")

    # @api.depends('patient_code', 'name')
    # def _compute_display_name(self):
    #     for rec in self:
    #         if rec.patient_code != "New":
    #             rec.display_name = f"[{rec.patient_code}]{rec.name}"
    #         else:
    #             rec.display_name = rec.name

    @api.model_create_multi
    def create(self, val_list):
        res = super(ResPatient, self).create(val_list)
        for record in res:
            new_partner = {
                'name': record.name,
                'phone': record.phone,
                'email': record.email,
                'mobile': record.mobile,
            }
            record.patient_code = self.env["ir.sequence"].next_by_code('res.patient')
            record.partner_id = self.env["res.partner"].create(new_partner)
        return res

    def write(self, vals):
        for record in self:
            if self.env.context.get('prevent_recursive_calls'):
                return super().write(vals)
            partners = self.env['res.partner'].search([('id','=',record.partner_id.id)])
            if record.partner_id:
                partner_data = {}
                if 'name' in vals.keys():
                    partner_data['name'] = vals.get('name')
                if 'phone' in vals.keys():
                    partner_data['phone'] = vals.get('phone')
                if 'email' in vals.keys():
                    partner_data['email'] = vals.get('email')
                if 'mobile' in vals.keys():
                    partner_data['mobile'] = vals.get('mobile')
                partners.with_context(prevent_recursive_calls=True).write(partner_data)
        res = super().write(vals)
        return res

    @api.onchange('date_of_birth')
    def select_patient_category(self):
        today = date.today()
        rd = relativedelta(today, self.date_of_birth)
        age = rd.years
        if age > 60:
            self.age_category = "Senior_Citizen"
        if age < 60 and age >= 18:
            self.age_category = "Adult"
        if age < 18 and age > 10:
            self.age_category = "Minor"
        if age <= 10:
            self.age_category = "Child"

    # def write(self, vals):
    #     if 'phone' in vals:
    #         if len(vals.get('phone')) != 10:
    #             raise UserError("Phone number should be 10 digits")
    #     res = super(ResPatient, self).write(vals)
    #     return res

    @api.constrains('phone')
    def validate_phone(self):
        for record in self:
            if record.phone and len(record.phone) != 10:
                raise UserError("Phone number should be 10 digits.")

            if record.phone:
                patient_ids = self.env['res.patient'].search_count([('phone', '=', record.phone)])
                if patient_ids > 1:
                    raise ValidationError("Phone number already exist.")

    def action_patient_appointment(self):
        view_id = self.env.ref('bista_hms.hms_appointment_from_view').id

        return {
            'name': 'Appointments',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'hms.appointment',
            'view_id': view_id,
            'target': 'current',
            'context': {'default_patient_id': self.id}
        }

    @api.constrains('date_of_birth')
    def validate_dob(self):
        for record in self:
            if record.date_of_birth > date.today():
                raise UserError("Birth date should be past date!")

    def action_calculate_age(self):
        today = date.today()
        rd = relativedelta(today, self.date_of_birth)
        self.age = f'{rd.years}Years {rd.months}Months {rd.days}Days'

    def _patient_counter(self):
        patient_count = self.env['res.patient'].search([('age', '>', 40)])
        print(len(patient_count))

    @api.depends("patient_ids.patient_id")
    def _action_appointment_count(self):
        for record in self:
            self.appointment_count = self.env["hms.appointment"].search_count([('patient_id', '=', record.id)])

    @api.depends("patient_ids.patient_id")
    def _action_prescription_count(self):
        for record in self:
            self.prescription_count = self.env["hms.prescription"].search_count([('patient_id', '=', record.id)])

    def action_open_view_of_appointment(self):
        form_view_id = self.env.ref('bista_hms.hms_appointment_from_view').id
        list_view_id = self.env.ref('bista_hms.appointment_list_view').id

        res = {
            'name': 'Appointments',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'hms.appointment',
            'target': 'current',
            'view_id': form_view_id,
            'context': {'default_patient_id': self.id}
        }

        if self.appointment_count >= 1:
            res['view_mode'] = 'list,form',
            res['views'] = [(list_view_id, 'list'), (form_view_id, 'form')]
            res['domain'] = [('patient_id', '=', self.id)]
            res['view_id'] = False

        return res

    def _weekly_auto_create_appointment(self):
        # patient_data = self.env['res.patient'].search([('weekly_visit','=',True),('weekly_visit_default_val','=',True)])
        patient_data = self.env['res.patient'].search([('weekly_visit', '=', True)])
        for record in patient_data:
            new_appointment_data = {
                'patient_id': record.id,
                'appointment_date': date.today() + timedelta(days=7),
            }
            # record.weekly_visit_default_val = False
            self.env["hms.appointment"].create(new_appointment_data)

    def action_open_prescription(self):
        form_view_id = self.env.ref('bista_hms.hms_prescription_from_view').id
        list_view_id = self.env.ref('bista_hms.hms_prescription_list_view').id

        res = {
            'name': 'Prescriptions',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'hms.prescription',
            'target': 'current',
            'view_id': form_view_id,
            'context': {'default_patient_id': self.id}
        }

        if self.prescription_count >= 1:
            res['view_mode'] = 'list,form',
            res['views'] = [(list_view_id, 'list'), (form_view_id, 'form')]
            res['domain'] = [('patient_id', '=', self.id)]
            res['view_id'] = False

        return res
