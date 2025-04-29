from odoo import fields,models,api

class SaleOrderDocument(models.Model):
    _name = "sale.order.document"
    _description = "This is our Model."


    product_ids = fields.Many2many("product.template",string="Products")
    document_id = fields.Many2one("documents.custom",string="Documents")
    sale_order_id = fields.Many2one("sale.order",string="Sale Order")
