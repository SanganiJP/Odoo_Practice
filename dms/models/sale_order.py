from odoo import fields,models,api

class SaleOrder(models.Model):
    _inherit = "sale.order"

    customer_tag_ids = fields.Many2many("documents.tag.master", string="Document Tags", store=True)
    document_tag_ids = fields.Many2many("documents.custom", string="Documents")
    doc_count = fields.Integer(string="Document Count", compute="_compute_doc_count", store=True)
    document_line_ids = fields.One2many("sale.order.document", "sale_order_id")

    @api.depends('document_tag_ids')
    def _compute_doc_count(self):
        # doc_count = 0
        # for doc in self.document_tag_ids:
        #     doc_count += 1
        for rec in self:
            rec.doc_count = len(rec.document_tag_ids)

    @api.onchange('partner_id')
    def get_customer_tags(self):
        self.customer_tag_ids = self.partner_id.tag_ids

    def get_document_tags(self):
        common_docs = self.env["documents.custom"]
        #
        # for line in self.order_line:
        #     for doc in line.product_template_id.doc_ids:
        #         if doc.tag_ids:
        #             for doc_tag in doc.tag_ids:
        #                 if doc_tag in self.customer_tag_ids:
        #                     common_docs |= doc
        #                     break;
        #
        # self.document_tag_ids = [(6, 0, common_docs.ids)]

        # for line in self.order_line:
        #     docs = line.product_template_id.doc_ids.filtered(lambda doc : any(tag in self.tag_ids for tag in doc.tag_ids))
        #     common_docs |= docs

        # product_doc = self.env['sale.order.document']

        products = self.env['product.template']

        for line in self.order_line:
            for doc in line.product_template_id.doc_ids:
                if doc.tag_ids:
                    for doc_tag in doc.tag_ids:
                        if doc_tag in self.customer_tag_ids:
                            products |= line.product_template_id
                            common_docs |= doc
                            break;

        self.document_tag_ids = [(6, 0, common_docs.ids)]

        for doc in common_docs:
            data = {
                'document_id': doc.id,
                'product_ids': products.ids,
                'sale_order_id': self.id,
            }
            self.env['sale.order.document'].create(data)



        # for doc in common_docs:
        #     self.env['sale.order.document'].create({'document_id': doc_tag, 'product_ids': products})

        # self.document_line_ids = [(6, 0, product_doc.ids)]

        # self.send_mail()


    def action_confirm(self):
        res = super().action_confirm()
        # common_docs = self.env["documents.custom"]
        # for line in self.move_ids:
        #     docs = line.product_template_id.doc_ids.filtered(lambda doc : any(tag in self.tag_ids for tag in doc.tag_ids))
        #     common_docs |= docs
        # self.picking_ids.document_tags_ids = [(6, 0, common_docs.ids)]
        self.picking_ids.document_tags_ids = self.document_tag_ids
        return res

    def send_mail(self):
        if self.user_id and self.user_id.login:
            template_id = self.env.ref('dms.email_template_for_get_documents')
            template_id.send_mail(self.id, force_send=True)