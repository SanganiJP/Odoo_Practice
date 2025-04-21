from odoo import models,fields,api


class RmaInvoiceLines(models.TransientModel):
    _name = "rma.invoice.lines"
    _description = "get invoice line data"

    product_id = fields.Many2one("product.product", string="Product")
    invoice_qty = fields.Integer(string="Invoice Qty")
    invoice_id = fields.Many2one("sale.rma.invoice.wizard",string="Invoice")
    available_for_invoice = fields.Integer(string="Available Qty")
