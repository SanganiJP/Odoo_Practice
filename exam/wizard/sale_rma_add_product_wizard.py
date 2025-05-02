from odoo import models,fields,api


class SaleRmaAddProductWizard(models.TransientModel):
    _name = "sale.rma.add.product.wizard"
    _description = "get invoice line data"

    # product_ids = fields.Many2many("product.product", string="Products")
    #
    #
    # def add_product_to_rma_line(self):
    #     ticket_id = self.env.context.get('active_id')
    #     if ticket_id:
    #         record = self.env['sale.rma'].browse(ticket_id)
    #         sale_order_lines = []
    #         for product in self.product_ids:
    #             sale_order_lines.append((0, 0, {
    #                 'product_id': product.id,
    #                 'sale_order_qty':1
    #             }))
    #         record.rma_line_ids = sale_order_lines


    # def add_product_to_sale_order(self):
        # ticket_id = self.env.context.get('active_id')
        # if ticket_id:
        #     record = self.env['sale.order'].browse(ticket_id)
        #     sale_order_lines = []
        #     for product in self.product_ids:
        #         sale_order_lines.append((0, 0, {
        #             'product_id': product.id,
        #         }))
        #     record.order_line = sale_order_lines