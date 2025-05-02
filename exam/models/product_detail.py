from odoo import fields, models, api


class ProductDetail(models.Model):
    _name = 'product.detail'
    _description = 'Description'

    product_ids = fields.Many2many('product.product', string="Orders")
    order_line_ids = fields.One2many("order.line", "order_line_id")

    @api.onchange('product_ids')
    def add_product_to_rma_line(self):
        order_lines = []
        order_lines = [(5, 0, 0)]
        for product in self.product_ids:
            order_lines.append((0, 0, {
                'name': product.id,
                'qty':1
            }))
        self.order_line_ids = order_lines