# -*- encoding: utf-8 -*-

from odoo import fields,models

class Project(models.Model):
    _name = "project.detail"
    _description = "Project Detail model"

    name = fields.Char(string="Project Name")
    project_lead_name = fields.Many2one("lead.info",string="Project Lead")
    project_type = fields.Many2one("project.types", string="Project Type")
    project_dept = fields.Many2one("project.dept", string="Project Department")