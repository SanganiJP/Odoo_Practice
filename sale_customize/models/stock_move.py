from odoo import fields,models,api

class StockMove(models.Model):
    _inherit = 'stock.move'

    # def _prepare_move_line_vals(self, quantity=None, reserved_quant=None):
    #     res = super()._prepare_move_line_vals()
    #     # res.update({'location_id':self.location_id.id})
    #     for move in self.sale_line_id:
    #         res['location_id'] = move.location_id.id
    #     return res