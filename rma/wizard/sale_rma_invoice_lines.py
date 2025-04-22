from odoo import models,fields,api
from odoo.exceptions import UserError


class RmaInvoiceLines(models.TransientModel):
    _name = "rma.invoice.lines"
    _description = "get invoice line data"

    product_id = fields.Many2one("product.product", string="Product")
    invoice_qty = fields.Integer(string="Invoice Qty")
    invoice_id = fields.Many2one("sale.rma.invoice.wizard",string="Invoice")
    available_for_invoice = fields.Integer(string="Available Qty")
    rma_line_id = fields.Many2one("sale.rma.line", string="RMA Line")

    @api.onchange('invoice_qty')
    def check_available_qty_to_invoice(self):
        if self.available_for_invoice < self.invoice_qty:
            raise UserError("You can't invoice more quantity then received quantity!")