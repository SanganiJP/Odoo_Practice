from odoo import fields,models,api

class StudentActivity(models.Model):
    _name = "student.activity"
    _description = "model"

    name = fields.Char(string="Activity")