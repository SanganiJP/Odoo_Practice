from odoo import fields,models,api

class StockPicking(models.Model):
    _inherit = "stock.picking"

    picking_id = fields.Many2one("sale.rma",string="Sale RMA")
