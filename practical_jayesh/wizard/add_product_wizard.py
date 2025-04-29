from odoo import models, fields, api


class AddProductWizard(models.TransientModel):
    _name = "add.product.wizard"
    _description = "line data"

    product_ids = fields.Many2many("product.product", string="Products")

    def add_product_to_order_line(self):
        """

        """
        ticket_id = self.env.context.get('active_id')
        if ticket_id:
            record = self.env['sale.order'].browse(ticket_id)
            sale_order_lines = []
            for product in self.product_ids:
                sale_order_lines.append((0, 0, {
                    'product_id': product.id,
                    'product_uom_qty': 1
                }))
            record.order_line = sale_order_lines




