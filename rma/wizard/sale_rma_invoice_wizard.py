from odoo import models,fields,api
from odoo.exceptions import UserError


class SaleRmaInvoiceWizard(models.TransientModel):
    _name = "sale.rma.invoice.wizard"

    ticket_id = fields.Many2one("sale.rma", string="Record ID")
    invoice_line_ids = fields.One2many("rma.invoice.lines","invoice_id",string=" Invoice Lines")

    def action_create_invoice(self):
        invoice_vals = self.prepare_invoices_vals()
        invoice_id = self.env['account.move'].create(invoice_vals)

        invoice_line_vals = self.prepare_invoices_lines_vals(invoice_id)
        self.env['account.move.line'].create(invoice_line_vals)

        if not invoice_line_vals:
            invoice_id.unlink()
            raise UserError('Please add invoice line!')

    def prepare_invoices_vals(self):
        self.ticket_id = self.env.context.get('active_id')
        values = {
            'move_type': 'out_invoice',
            'invoice_date': self.ticket_id.date,
            'partner_id': self.ticket_id.sale_order_id.partner_id.id,
            'partner_shipping_id': self.ticket_id.sale_order_id.partner_id.id,
            'company_id': self.ticket_id.env.company.id,
            'user_id': self.ticket_id.env.user.id,
            'rma_invoice_id': self.ticket_id.id,
            }
        return values

    def prepare_invoices_lines_vals(self, invoice_id):
        line_val = []
        for line in self.invoice_line_ids:
            if line.invoice_qty > 0:
                line_vals = {
                    'product_id': line.product_id.id,
                    'quantity': line.invoice_qty,
                    'move_id': invoice_id.id,
                    'account_move_line_id': line.rma_line_id.id,
                }
                line_val.append(line_vals)
        return line_val

    @api.onchange('ticket_id')
    def onchange_sale_order(self):
        self.ticket_id = self.env.context.get('active_id')
        if self.ticket_id:
            records = self.env['sale.rma'].browse(self.ticket_id.id)
            rma_lines = []
            for line in records.rma_line_ids:
                if line.available_qty_to_invoice > 0:
                    rma_lines.append((0, 0, {
                        'product_id': line.product_id.id,
                        'invoice_qty': line.available_qty_to_invoice,
                        'available_for_invoice': line.available_qty_to_invoice,
                        'rma_line_id': line.id,
                    }))
            self.invoice_line_ids = rma_lines

