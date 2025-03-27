from odoo import fields,models,api

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.depends('product_id', 'product_uom', 'product_uom_qty', 'order_id.partner_id')
    def _compute_discount(self):
        res = super(SaleOrderLine, self)._compute_discount()
        for line in self:
            line.discount += line.order_id.partner_id.extra_discount
        return res