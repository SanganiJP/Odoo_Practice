from odoo import fields, models, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    location_id = fields.Many2one("stock.location", string="Location")

    # def _prepare_move_line_vals(self, quantity=None, reserved_quant=None):
    #     res = super()._prepare_move_line_vals()
    #     # res.update({'location_id':self.location_id.id})
    #     res['location_id'] = self.location_id.id
    #     return res

    # def _prepare_procurement_values(self, group_id=False):
    #     values = super()._prepare_procurement_values(group_id=group_id)
    #     if self.location_id:
    #         values['location_final_id'] = self.location_id
    #     return values

    # @api.depends('product_id', 'product_uom', 'product_uom_qty')
    # def _compute_pricelist_item_id(self):
    #     res = super().
    #     for line in self:
    #         if not line.product_id or line.display_type or not line.order_id.pricelist_id:
    #             line.pricelist_item_id = False
    #         else:
    #             line.pricelist_item_id = line.order_id.pricelist_id._get_product_rule(
    #                 line.product_id,
    #                 quantity=line.product_uom_qty or 1.0,
    #                 uom=line.product_uom,
    #                 date=line._get_order_date(),
    #             )

    def _get_pricelist_price(self):
        res = super()._get_pricelist_price()

        for line in self:
            pricelist_id = self.env['product.pricelist'].search([('is_active', '=', True)])
            if pricelist_id:
                active_pricelist_id = pricelist_id._get_product_rule(
                    line.product_id,
                    quantity=line.product_uom_qty or 1.0,
                    uom=line.product_uom,
                    date=line._get_order_date(),
                )

                active_pricelist_rec = self.env['product.pricelist.item'].browse(active_pricelist_id)
                if active_pricelist_rec:
                    new_price = active_pricelist_rec._compute_price(
                        product=self.product_id.with_context(**self._get_product_price_context()),
                        quantity=self.product_uom_qty or 1.0,
                        uom=self.product_uom,
                        date=self._get_order_date(),
                        currency=self.currency_id,
                    )
                    # price_according_current_price = res
                    # print(price_according_current_price)
                    # print(new_price)

                    return max(res, new_price)

            return res
