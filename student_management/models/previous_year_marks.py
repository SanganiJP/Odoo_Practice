# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class ResSubject(models.Model):
    _name = 'previous.year.marks'
    _description = 'student_management.previous.year.mark'
    _rec_name = "previous_year_marks_id"

    previous_year_marks_id = fields.Many2one("res.student",string="Name")
    subject_name = fields.Many2one("subject.subject",string="Subject Name", required=True)
    total_marks = fields.Float(string="Total marks",required=True)
    obtained_marks_in_exam = fields.Float(string="Obtained Marks In Exam",required=True)
    obtained_marks_in_viva = fields.Float(string="Obtained Marks In Viva",required=True)
    total_obtained_marks = fields.Float(string="Total Obtained Marks",compute="_compute_total_obtained_marks", store=True)


    @api.constrains('obtained_marks_in_exam')
    def validate_exam_marks(self):
        for rec in self:
            if rec.obtained_marks_in_exam > 80:
                raise UserError("Exam marks must be less then 80.")

    @api.depends('obtained_marks_in_exam','obtained_marks_in_viva')
    def _compute_total_obtained_marks(self):
        for rec in self:
            if rec.obtained_marks_in_exam and rec.obtained_marks_in_viva:
                rec.total_obtained_marks = rec.obtained_marks_in_exam + rec.obtained_marks_in_viva



