from odoo import fields, models, api


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"
    _description = "Purchase Order"

    service_type_product_qty = fields.Integer(string="Service Product Qty", compute="_compute_service_type_product_qty", store=True)

    @api.depends('order_line.product_id')
    def _compute_service_type_product_qty(self):
        for rec in self:
            rec.service_type_product_qty = sum(rec.order_line.filtered(lambda line: line.product_id.type == 'service').mapped('product_qty'))


