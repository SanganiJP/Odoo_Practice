from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    sequence_id = fields.Many2one("ir.sequence", string="Product Sequence")