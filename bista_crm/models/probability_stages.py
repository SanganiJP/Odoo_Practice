from odoo import fields,models,api

class ProbabilityStage(models.Model):
    _name = "probability.stages"
    _description = "model"

    name = fields.Char(string="Stage Name")
    percentage = fields.Integer(string="Stage Percentage")
