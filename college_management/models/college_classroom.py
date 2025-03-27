# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CollegeClassroom(models.Model):
    _name = "college.classroom"
    _description = "College classroom model"

    name = fields.Char(string="Classroom Name", requried=True)
    teacher_id = fields.Many2one("college.teacher", string="Teacher Name")
    student_ids = fields.One2many("college.student","classroom_id", string="Classroom Details")
    total_student = fields.Integer(string="Total Student",compute="_compute_total_students", store=True)

    @api.depends('student_ids')
    def _compute_total_students(self):
        for rec in self:
            total_students = self.env["college.student"].search_count([('classroom_id','=',rec.id)])
            rec.total_student = total_students

    def action_open_student_list_view(self):
        from_id = self.env.ref('college_management.college_student_from_view').id
        list_id = self.env.ref('college_management.college_student_list_view').id

        return {
            'name': 'Classroom',
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            # 'view_mode': 'list',
            'res_model': 'college.student',
            # 'view_id': view_id,
            # 'view_id': list_id,
            'views': [(list_id, 'list'), (from_id, 'form')],
            'target': 'current',
            'domain': [('classroom_id', '=', self.id)]
            # 'context': {'default_patient_id': self.id}
        }






