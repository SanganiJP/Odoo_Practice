from datetime import date
from odoo import fields, models, api
from odoo.exceptions import UserError


class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'
    _description = 'Pay'

    def action_create_payments(self):
        res = super().action_create_payments()
        rec_id = self.env.context.get('active_id')
        today = date.today()
        record = self.env['account.move'].browse(rec_id)
        if record.loan_id:
            if record.amount_residual > self.amount:
                raise UserError('You must have to pay full EMI Amount!')
            emi_line_rec = self.env['emi.lines'].search([('loan_id', '=', record.loan_id.id), ('emi_date', '=', today)])
            emi_line_rec.write({'state': 'paid'})
        return res
