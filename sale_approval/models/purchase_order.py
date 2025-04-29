from odoo import fields,models,api

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    product_category = fields.Many2one("product.category", string="Product Category")