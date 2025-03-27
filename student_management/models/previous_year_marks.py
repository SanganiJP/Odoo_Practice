# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResSubject(models.Model):
    _name = 'previous.year.marks'
    _description = 'student_management.previous.year.mark'
    _rec_name = "previous_year_marks_id"

    previous_year_marks_id = fields.Many2one("res.student",string="Name")
    subject_name = fields.Many2one("subject.subject",string="Subject Name", requried=True)
    total_marks = fields.Float(string="Total marks",requried=True)
    obtained_marks_in_exam = fields.Float(string="Obtained Marks In Exam",requried=True)
    obtained_marks_in_viva = fields.Float(string="Obtained Marks In Viva",requried=True)
    total_obtained_marks = fields.Float(string="Total Obtained Marks",compute="_compute_total_obtained_marks", store=True)

    @api.depends('obtained_marks_in_exam','obtained_marks_in_viva')
    def _compute_total_obtained_marks(self):
        for rec in self:
            if rec.obtained_marks_in_exam and rec.obtained_marks_in_viva:
                rec.total_obtained_marks = rec.obtained_marks_in_exam + rec.obtained_marks_in_viva



