from odoo import fields,models,api

class SaleOrder(models.Model):
    _inherit = "sale.order"

    note = fields.Text(string="Extra Note")
    previous_price = fields.Float(string="Previous Price")