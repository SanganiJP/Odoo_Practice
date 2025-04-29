from odoo import models, fields, api


class AddProductWizard(models.TransientModel):
    _name = "add.product.wizard"
    _description = "add product wizard"

    product_ids = fields.Many2many("product.product", string="Product")

    def add_product_to_sale_order(self):
        ticket_id = self.env.context.get('active_id')
        if ticket_id:
            record = self.env['sale.order'].browse(ticket_id)
            sale_order_lines = []
            for product in self.product_ids:
                sale_order_lines.append((0, 0, {
                    'product_id': product.id,
                }))
            record.order_line = sale_order_lines
                # ticket_id.order_line = sale_order_lines
