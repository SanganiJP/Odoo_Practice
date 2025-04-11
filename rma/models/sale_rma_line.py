from odoo import fields,models,api

class SaleRmaLines(models.Model):
    _name = "sale.rma.line"
    _description = "sale rma line model"

    product_id = fields.Many2one("product.product",string="Product")
    sale_order_qty = fields.Integer(string="SO Qty")
    unit_price = fields.Float(string="Unit Price")
    to_receive = fields.Integer(string="To Receive")
    received_qty = fields.Integer(string="Receive Qty")
    rma_id = fields.Many2one("sale.rma",string="Order ID")

