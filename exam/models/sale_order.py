from odoo import fields,models,api

class SaleOrder(models.Model):
    _inherit = "sale.order"

    # customer_tag_ids = fields.Many2many("documents.tag.master", string="Document Tags", store=True)
    # document_tag_ids = fields.Many2many("documents.custom", string="Documents")
    # doc_count = fields.Integer(string="Document Count", compute="_compute_doc_count", store=True)
    # document_line_ids = fields.One2many("sale.order.document", "sale_order_id")

    # @api.depends('document_tag_ids')
    # def _compute_doc_count(self):
    #     # doc_count = 0
    #     # for doc in self.document_tag_ids:
    #     #     doc_count += 1
    #     for rec in self:
    #         rec.doc_count = len(rec.document_tag_ids)
    #
    # @api.onchange('partner_id')
    # def get_customer_tags(self):
    #     self.customer_tag_ids = self.partner_id.tag_ids
    #
    #
    # def send_mail(self):
    #     if self.user_id and self.user_id.login:
    #         template_id = self.env.ref('dms.email_template_for_get_documents')
    #         template_id.send_mail(self.id, force_send=True)