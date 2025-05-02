from odoo import fields, models, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    # previous_price = fields.Float(string="Previous Price", compute='_compute_previous_price')
    # # warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse')
    # available_qty = fields.Integer(string="WH Available Qty", compute='_compute_quantities')
    # wh_location = fields.Many2many('stock.location', string="WH Location")
    # available_qty_wh_loc = fields.Integer(string="WH Loc Available Qty", compute='_compute_quantities')
    #
    # @api.depends('product_id', 'product_uom', 'product_uom_qty', 'order_id.partner_id')
    # def _compute_discount(self):
    #     res = super(SaleOrderLine, self)._compute_discount()
    #     for line in self:
    #         line.discount += line.order_id.partner_id.extra_discount
    #     return res
    #
    # @api.depends('product_template_id', 'product_id')
    # def _compute_previous_price(self):
    #     for rec in self:
    #         rec.previous_price = rec.product_id.lst_price
    #
    # def _compute_quantities(self):
    #     for rec in self:
    #         if rec.wh_location.ids:
    #             rec.available_qty_wh_loc = rec.product_id.with_context(location=rec.wh_location.ids).qty_available
    #         else:
    #             rec.available_qty_wh_loc = 0
    #         rec.available_qty = rec.product_id.with_context(warehouse_id=rec.order_id.warehouse_id.id).qty_available
    #         # rec.available_qty = rec.product_id.with_context({'warehouse_id': rec.order_id.warehouse_id.id}).qty_available
