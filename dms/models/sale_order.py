from odoo import fields,models,api

class SaleOrder(models.Model):
    _inherit = "sale.order"

    customer_tag_ids = fields.Many2many("documents.tag.master", string="Customer Tags", store=True)
    document_ids = fields.Many2many("documents.custom", string="Document Tags")

    @api.onchange('partner_id')
    def get_customer_tags(self):
        self.customer_tag_ids = self.partner_id.tag_ids



