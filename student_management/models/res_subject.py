# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResSubject(models.Model):
    _name = 'subject.subject'
    _description = 'student_management.subject.subject'

    name = fields.Char(string="Subject Name")