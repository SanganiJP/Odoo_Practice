# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CollegeTeacher(models.Model):
    _name = "college.teacher"
    _description = "College teacher model"

    name = fields.Char(string="Teacher Name")
    subject = fields.Char(string="Subject")
    classroom_ids = fields.One2many("college.classroom","teacher_id",string="Teachers")
    total_classroom = fields.Integer(string="Total Classroom", compute='_compute_total_classroom', store=True)

    @api.depends('classroom_ids')
    def _compute_total_classroom(self):
        for rec in self:
            count = self.env["college.classroom"].search_count([('teacher_id','=', rec.id)])
            rec.total_classroom = count
