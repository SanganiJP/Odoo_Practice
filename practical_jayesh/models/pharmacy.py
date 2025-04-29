from odoo import fields, models, api


class Pharmacy(models.Model):
    _name = 'pharmacy'
    _description = 'Description'

    name = fields.Char(string="Name", copy=False)
    product_ids = fields.One2many("product.template","pharma_product_id",string="Products")
