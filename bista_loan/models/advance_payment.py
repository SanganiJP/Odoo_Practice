from odoo import fields,models,api

class AdvancePayment(models.Model):
    _name = "advance.payment"
    _description = "Advance Payment"

    payment_date = fields.Date(string="Date")
    payment_amount = fields.Float(string="Amount")
    loan_id = fields.Many2one("loan.system", string="Loan ID")
    is_paid = fields.Boolean(default=False, string="Is Paid")

    def process_advance_payment(self):
        return self.loan_id.action_generate_advance_payment_bill(self)
