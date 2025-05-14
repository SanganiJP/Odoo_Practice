from odoo import fields, models, api


class LoanInterestRate(models.Model):
    _name = 'loan.interest.rate'
    _description = 'Description'

    loan_id = fields.Many2one("loan.system", string="Loan ID")
    interest_rate = fields.Float(string="Interest Rate")
    is_active = fields.Boolean(string="Active")
    date = fields.Date(string="Date", required=True)
    # today =

    def activate_interest_rate(self):
        self.loan_id.current_interest_rate = self.interest_rate
        old_ir = self.env['loan.interest.rate'].search([('is_active','=',True), ('loan_id', '=', self.loan_id.id)])
        old_ir.write({'is_active': False})
        self.is_active = True


