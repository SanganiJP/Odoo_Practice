from odoo import fields,models,api

class TeamRma(models.Model):
    _name = "team.rma"
    _description = "order return process"
    _rec_name = "team_name"

    team_name = fields.Char(string="Team Name")
    team_prefix = fields.Char(string="Prefix")


