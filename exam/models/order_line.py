from odoo import fields, models, api


class OrderLine(models.Model):
    _name = 'order.line'
    _description = 'Description'

    name = fields.Many2one("product.product", string="Product")
    qty = fields.Integer(string="Quantity")
    order_line_id = fields.Many2one("product.detail", string="order")
