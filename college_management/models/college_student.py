# -*- coding: utf-8 -*-
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class CollegeStudent(models.Model):
    _name = "college.student"
    _description = "College Student model"

    name = fields.Char(string="Student Name", required=True)
    dob = fields.Date(string="Date of birth")
    age = fields.Integer(string="Age", compute="_compute_student_age", store=True)
    phone = fields.Char(string="Phone")
    grade = fields.Char(string="Grade")
    classroom_id = fields.Many2one("college.classroom",string="Classroom")

    @api.depends('dob')
    def _compute_student_age(self):
        for rec in self:
            today = date.today()
            difference = relativedelta(today, self.dob)
            # print(difference.years)
            rec.age = difference.years

    @api.constrains('phone')
    def validate_phone(self):
        for record in self:
            if record.phone and len(record.phone) != 10:
                raise UserError("Phone number should be 10 digits.")

            if record.phone:
                patient_ids = self.env['college.student'].search_count([('phone', '=', record.phone)])
                if patient_ids > 1:
                    raise UserError("Phone number already exist.")


