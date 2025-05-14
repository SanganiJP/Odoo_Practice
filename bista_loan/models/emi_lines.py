from odoo import fields, models, api

STATUS = [('pending', 'Pending'),
          ('invoiced', 'Invoiced'),
          ('paid', 'Paid')]

class EmiLines(models.Model):
    _name = 'emi.lines'
    _description = 'Description'

    loan_id = fields.Many2one("loan.system", string="Loan ID")
    emi_date = fields.Date(string="Date")
    principal_paid = fields.Float(string="Principal Paid")
    interest_charged = fields.Float(string="Interest Charged")
    total_payment = fields.Float(string="Total Payment")
    balance = fields.Float(string="Balance")
    state = fields.Selection(STATUS, string="Status", default='pending')

