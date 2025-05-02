from odoo import fields,models,api

class CrmLead(models.Model):
    _inherit = "crm.lead"

    # products_ids = fields.Many2many("product.template",string="Products")