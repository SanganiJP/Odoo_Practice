# -*- encoding: utf-8 -*-

from odoo import fields,models

class Projecttype(models.Model):
    _name = "project.types"
    _description = "Project type selection model"

    name = fields.Char(string="Project Type")
    project_types_ids = fields.One2many("project.detail","project_type",string="Project types")
