from odoo import models,fields,api
from odoo.exceptions import UserError


class WizardRmaLines(models.TransientModel):
    _name = "wizard.rma.lines"
    _description = "get rma line data"

    wizard_rma_line_id = fields.Many2one("rma.wizard",string="RMA Line ID")
    product_id = fields.Many2one("product.product", string="Product")
    so_qty = fields.Integer(string="SO Qty")
    qty = fields.Integer(string="Return Qty")
    rma_lines_id = fields.Many2one("sale.rma.line", string="RMA Line ID")
    available_qty = fields.Integer(string="Available Qty", store=True)


    @api.onchange('qty')
    def check_return_qty(self):
        if self.available_qty < self.qty:
            raise UserError("You can't return more quantity then ordered quantity!")
