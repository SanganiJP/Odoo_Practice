from odoo import fields,models,api

class StockRule(models.Model):
    _inherit = 'stock.rule'
    
    # def _get_stock_move_values(self, product_id, product_qty, product_uom, location_dest_id, name, origin, company_id, values):
    #     move_vals = super()._get_stock_move_values()
    #     return super()._get_stock_move_values()