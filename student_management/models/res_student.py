# -*- coding: utf-8 -*-
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api
from odoo.exceptions import UserError


class ResStudent(models.Model):
    _name = 'res.student'
    _description = 'student_management.student_management'

    name = fields.Char(string="Name", required=True)
    registration_id = fields.Char(string="Registration ID", copy=False, readonly=True, index=True, default="New")
    registration_date = fields.Date(string="Registration Date", required=True)
    date_of_birth = fields.Date(string="Birth Date", required=True)
    student_age = fields.Char(string="Age", compute="_compute_student_age", store=True)
    age = fields.Integer(string="Age", default=11)
    phone = fields.Char(string="Phone No")
    email_id = fields.Char(string="Email")
    standard = fields.Selection(
        [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'),
         ('10', '10'), ('11', '11'), ('12', '12')],
        string="Standard", default='1')
    guardian_name = fields.Char(string="Guardian Name")
    guardian_phone = fields.Char(string="guardian_phone")
    # tuition_fee_structure = fields.Many2one("",string="Tuition Fee Structure")
    is_blocked = fields.Boolean(string="Is Blocked")
    is_expired = fields.Boolean(string="Is Expired")
    previous_year_marks = fields.One2many("previous.year.marks", "previous_year_marks_id", string="Previous year mark")
    tuition_free_structure = fields.Many2one("tuition.fee.structure", string="Tuition free structure",
                                             domain="[('standard','=',standard)]")

    @api.model_create_multi
    def create(self, val_list):
        res = super(ResStudent, self).create(val_list)
        for record in res:
            record.registration_id = self.env["ir.sequence"].next_by_code('res.student')
        return res

    @api.depends('date_of_birth')
    def _compute_student_age(self):
        for rec in self:
            if rec.date_of_birth:
                today = date.today()
                difference = relativedelta(today, self.date_of_birth)
                rec.student_age = f'{difference.years}Years, {difference.months}Months'
                rec.age = difference.years

    @api.constrains('phone')
    def validate_phone(self):
        for record in self:
            if not record.phone.isdigit():
                raise UserError("Phone number must contain digit!")

            if record.phone and len(record.phone) != 10:
                raise UserError("Phone number should be 10 digits.")

            if record.phone:
                patient_ids = self.env['res.student'].search_count([('phone', '=', record.phone)])
                if patient_ids > 1:
                    raise UserError("Phone number already exist.")


            #     record.phone.isdigit()
            #     phone = record.phone
            #     for digit in range(10):
            #         if phone[digit] in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
            #             digit += 1
            #         else:

    def action_unblock_student(self):
        self.is_blocked = False

    def action_block_student(self):
        self.is_blocked = True

    def _schedule_action_registration_expired(self):
        start_of_month = date.today() - timedelta(days=30)

        students = self.env["res.student"].search([
            ('registration_date', '<', start_of_month),
            ('is_blocked', '=', False)
        ])
        students.write({'is_expired': True})

        # students = self.env["res.student"].search([],)
        # print(students)
        # students.is_expired = True

    def write(self, vals):
        for rec in self:
            if rec.is_blocked:
                if 'is_blocked' not in  vals.keys():
                    raise UserError("You cannot edit a blocked record.")
        res = super(ResStudent, self).write(vals)
        return res
