from odoo import fields, models, api

class LoanApprovalTeam(models.Model):
    _name = 'loan.approval.team'
    _description = 'Description'

    name = fields.Char(string="Team Name")
    approval_level_ids = fields.One2many('approval.levels',"team_id", string="Approval Level")