from odoo import fields,models,api

class StockPicking(models.Model):
    _inherit = "stock.picking"

    # document_tags_ids = fields.Many2many("documents.custom", string="Document Tags")

