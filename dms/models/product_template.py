from odoo import fields,models,api

class ProductTemplate(models.Model):
    _inherit = "product.template"

    doc_ids = fields.Many2many("documents.custom", string="Documents Tags")
