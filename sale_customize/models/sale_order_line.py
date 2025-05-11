from odoo import fields, models, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    location_id = fields.Many2one("stock.location",string="Location")

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