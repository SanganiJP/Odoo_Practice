from itertools import count

from dateutil.relativedelta import relativedelta
from odoo import fields, models, api
from odoo.exceptions import UserError
from datetime import date

from odoo.fields import Many2one

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

GUARDIAN_TYPE = [('parent','Parent'),
                ('Sibling','Sibling'),
                ('Relative','Relative'),
                ('Friend','Friend'),
                ('Other','Other')]

class ResPatient(models.Model):
    _name = "res.patient"
    _description = "Patient Model"

    name = fields.Char(string="Name", required=True)
    patient_code = fields.Char(string="Patient ID", default="New")
    blood_group = fields.Selection(BLOOD_GROUP, string="Blood Group", required=True)
    date_of_birth = fields.Date(string="DOB", required=True)
    age = fields.Char(string="Age")
    previous_diseases = fields.Text(string="Previous Diseases")
    phone = fields.Char(string="Phone", required=True)
    email = fields.Char(string="Email")
    mobile = fields.Char(string="Mobile")
    age_category = fields.Selection(AGE_CATEGORY, string="Patient Category")
    guardian_type = fields.Selection(GUARDIAN_TYPE, string="Guardian")
    guardian_id = fields.Many2one("res.partner", string="Guardian Name")
    patient_ids = fields.One2many("hms.appointment", "patient_id",string="Patient Appointments")

    @api.model_create_multi
    def create(self, val_list):
        res = super(ResPatient, self).create(val_list)
        for record in res:
            record.patient_code = self.env["ir.sequence"].next_by_code('res.patient')
        return res
        # for val in val_list:
        #     val.update({'patient_code':self.env["ir.sequence"].next_by_code('res.patient')})
        # res = super(ResPatient, self).create(val_list)
        # return res

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

    # @api.onchange('age_category')
    # def select_guardian_filed(self):
    #     if self.age_category in ['Child','Minor']:
    #         if not self.guardian_type:
    #             raise UserError("Please select your guardian!")

    # def write(self, vals):
    #     if 'phone' in vals:
    #        if len(vals.get('phone')) != 10:
    #            raise UserError("Phone number should be 10 digits")
    #     res = super(ResPatient, self).write(vals)
    #     return res

    @api.constrains('phone')
    def validate_phone(self):
        # print(self.phone)
        if len(self.phone) != 10:
            raise UserError("Phone number should be 10 digits.")

    def action_patient_appointment(self):
        view_id = self.env.ref('bista_hms.hms_appointment_from_view').id

        return {
            'name': 'Appointments',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'hms.appointment',
            'view_id': view_id,
            'target': 'current',
            'context': {'default_patient_id': self.id, 'child': True}
        }

    @api.constrains('date_of_birth')
    def validate_dob(self):
        if self.date_of_birth > date.today():
            raise UserError("Birth date should be past date!")

    def action_calculate_age(self):
        # dob_year = self.date_of_birth.year
        # current_year = date.today().year
        # age = current_year - dob_year
        # self.age = f'{age}Years'
        # dob = date(self.date_of_birth.year,self.date_of_birth.month,self.date_of_birth.day)
        # current_date = date.today()
        # date_difference = current_date - dob
        # d = date_difference.days
        # m = int(d/30.55)
        # y = int(d/365.25)
        # month1 = m - y*12
        # self.age = f'{y}Years {month1}Month'

        today = date.today()
        rd = relativedelta(today, self.date_of_birth)
        self.age = f'{rd.years}Years {rd.months}Months {rd.days}Days'

    def _patient_counter(self):
        patient_count = self.env['res.patient'].search([('age', '>', 40)])
        print(len(patient_count))