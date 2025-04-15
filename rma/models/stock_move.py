from odoo import fields, models, api

class StockMove(models.Model):
    _inherit = "stock.move"

    move_line_id = fields.Many2one("sale.rma.line", string="RMA Line")
