from odoo import fields,models,api

class StockPicking(models.Model):
    _inherit = "stock.picking"


    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        return res