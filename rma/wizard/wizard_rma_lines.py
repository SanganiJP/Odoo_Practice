from odoo import models,fields,api

class WizardRmaLines(models.TransientModel):
    _name = "wizard.rma.lines"
    _description = "get rma line data"

    wizard_rma_line_id = fields.Many2one("rma.wizard",string="RMA Line ID")
    product_id = fields.Many2one("product.product", string="Product")
    so_qty = fields.Integer(string="SO Qty")
    qty = fields.Integer(string="Quantity")
