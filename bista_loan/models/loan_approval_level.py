from odoo import fields, models, api

STATUS = [('pending', 'Pending'),
          ('to_approve', 'To Approve'),
          ('rejected', 'Rejected'),
          ('approved', 'Approved')]

class LoanApprovalLevel(models.Model):
    _name = 'loan.approval.level'
    _description = 'Description'

    name = fields.Char(string="Approval Level")
    team_member = fields.Many2many('res.users', string="Team Member")
    team_level = fields.Integer(string="Level", store=True)
    approved_by = fields.Many2one("res.users",string="Approved By")
    rejected_by = fields.Many2one("res.users",string="Rejected By")
    approve_time = fields.Datetime(string="Approve Date")
    loan_approve_stage = fields.Selection(STATUS, string="Status", default='pending')
    loan_id = fields.Many2one("loan.system",string="Loan Name")

