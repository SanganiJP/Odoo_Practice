from odoo import fields,models,api

class ProductTemplate(models.Model):
    _inherit = "product.template"
    
    pharma_product_id = fields.Many2one("pharmacy",string="Pharmacy Product")
