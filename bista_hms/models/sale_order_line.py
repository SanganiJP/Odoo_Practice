from odoo import fields,models,api

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    previous_price = fields.Float(string="Previous Price", compute='_compute_previous_price')

    @api.depends('product_id', 'product_uom', 'product_uom_qty', 'order_id.partner_id')
    def _compute_discount(self):
        res = super(SaleOrderLine, self)._compute_discount()
        for line in self:
            line.discount += line.order_id.partner_id.extra_discount
        return res

    @api.depends('product_template_id','product_id')
    def _compute_previous_price(self):
        for rec in self:
            rec.previous_price = rec.product_id.lst_price
