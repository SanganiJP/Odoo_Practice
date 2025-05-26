from odoo import api, fields, models
from odoo.exceptions import UserError


class AccountPayment(models.Model):
    _inherit = "account.payment"

    remaining_amount = fields.Float(compute='_compute_remaining_amount', string="Remaining Amount", store=True)
    invoice_rec_ids = fields.One2many("account.invoice.records", "payment_id", string="Invoices")

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        if self.partner_id:
            invoices_rec_list = []
            self.invoice_rec_ids = False
            invoices = self.env['account.move'].search(
                [('partner_id', '=', self.partner_id.id), ('amount_residual', '>', 0), ('move_type', '=', 'out_invoice'), ('state', '=', 'posted')])
            for invoice in invoices:
                invoices_rec_list.append((0, 0, {
                    'name': invoice.name,
                    'due_amount': invoice.amount_residual,
                    'date': invoice.invoice_date,
                }))
            self.invoice_rec_ids = invoices_rec_list

    @api.onchange('amount')
    def onchange_amount(self):
        allocatable_amount = self.amount
        for invoice in self.invoice_rec_ids:
            if allocatable_amount == 0:
                invoice.allocation_amount = 0

            elif allocatable_amount - invoice.due_amount > 0:
                invoice.allocation_amount = invoice.due_amount

            elif allocatable_amount - invoice.due_amount < 0:
                invoice.allocation_amount = allocatable_amount

            allocatable_amount -= invoice.allocation_amount

    @api.depends('invoice_rec_ids.allocation_amount')
    def _compute_remaining_amount(self):
        for rec in self:
            if rec.amount and rec.invoice_rec_ids:
                allocated_amount = sum(rec.invoice_rec_ids.mapped('allocation_amount'))
                if rec.amount - allocated_amount >= 0:
                    rec.remaining_amount = rec.amount - allocated_amount
                else:
                    raise UserError("There is no amount left to allocate.")
            else:
                self.remaining_amount = 0

    # self.ensure_one()
    # lines = self.env['account.move.line'].browse(line_id)
    # lines += self.line_ids.filtered(lambda line: line.account_id == lines[0].account_id and not line.reconciled)
    # return lines.reconcile()

    def action_post(self):
        res = super().action_post()
        # line_id = self.move_id.line_ids.filtered(lambda line : line.credit > 0)
        # for invoice in self.invoice_rec_ids:
        #     invoice_id = self.env['account.move'].search([('name','=',invoice.name)])
        #     invoice_id.js_assign_outstanding_line(line_id.id)
        return res