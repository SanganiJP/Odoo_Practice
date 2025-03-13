from itertools import count

from dateutil.relativedelta import relativedelta

from odoo import fields, models, api
from odoo.exceptions import UserError
from datetime import date

BLOOD_GROUP = [('A+', 'A+ve'),
               ('B+', 'B+ve'),
               ('O+', 'O+ve'),
               ('AB+', 'AB+ve'),
               ('A-', 'A-ve'),
               ('B-', 'B-ve'),
               ('O-', 'O-ve'),
               ('AB-', 'AB-ve')]


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
        #
        # d = date_difference.days
        # m = int(d/30.55)
        # y = int(d/365.25)
        # month1 = m - y*12
        # self.age = f'{y}Years {month1}Month'

        today = date.today()
        rd = relativedelta(today, self.date_of_birth)
        self.age = f'{rd.years}Years {rd.months}Months'