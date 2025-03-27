from datetime import datetime, date

from PIL.ImageChops import difference
from dateutil.relativedelta import relativedelta

from odoo import models,fields,api

class DatePracticeWizard(models.TransientModel):
    _name = "date.practice.wizard"
    _description = "Date Practice Wizard"

    # name = fields.Char(string="Name")
    date_of_birth = fields.Datetime(string="Date of Birth", required=True)
    current_date = fields.Datetime(string="Current Date", default=datetime.now())
    dob = fields.Date(string="Date of Birth", required=True)
    my_age = fields.Float(string="My Age")

    age = fields.Char(string="Age")

    @api.onchange('date_of_birth')
    def count_age_from_dob(self):
        if self.date_of_birth:
            # diff = relativedelta(self.current_date, self.date_of_birth)
            # self.age = f'{diff.years}years, {diff.months}month,{diff.days}days'
            date_difference = self.current_date - self.date_of_birth
            self.age = int(date_difference.total_seconds()/(365.25 * 24 * 60 * 60))

    @api.onchange('dob')
    def find_age(self):
        if self.dob:
            self.my_age = (date.today() - self.dob).days


     # def find_draft_state_time(self):
     #        diff = datetime.now() - self.draft_state_start_time
     #        total_hours = int(diff.total_seconds() / 3600)
     #        return total_hours