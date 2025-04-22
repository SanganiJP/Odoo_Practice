from odoo import fields,models,api

class SaleOrder(models.Model):
    _inherit = "sale.order"

    customer_tag_ids = fields.Many2many("documents.tag.master", string="Customer Tags", store=True)
    document_tag_ids = fields.Many2many("documents.custom", string="Document Tags")

    @api.onchange('partner_id')
    def get_customer_tags(self):
        self.customer_tag_ids = self.partner_id.tag_ids

    def get_document_tags(self):
        common_docs = self.env["documents.custom"]

        for line in self.order_line:
            for doc in line.product_template_id.doc_ids:
                if doc.tag_ids:
                    for doc_tag in doc.tag_ids:
                        if doc_tag in self.customer_tag_ids:
                            common_docs |= doc
                            break;

        # for line in self.order_line:
        #     docs = line.product_template_id.doc_ids.filtered(lambda doc : any(tag in self.tag_ids for tag in doc.tag_ids))
        #     common_docs |= docs

        self.document_tag_ids = [(6, 0, common_docs.ids)]

    def action_confirm(self):
        res = super().action_confirm()
        # common_docs = self.env["documents.custom"]
        # for line in self.move_ids:
        #     docs = line.product_template_id.doc_ids.filtered(lambda doc : any(tag in self.tag_ids for tag in doc.tag_ids))
        #     common_docs |= docs
        # self.picking_ids.document_tags_ids = [(6, 0, common_docs.ids)]
        self.picking_ids.document_tags_ids = self.document_tag_ids
        return res


