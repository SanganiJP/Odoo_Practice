# -*- encoding: utf-8 -*-

from odoo import fields,models

class school(models.Model):
    _name = "school.details"
    _description = "School details model"

    name = fields.Char(String="Name")
