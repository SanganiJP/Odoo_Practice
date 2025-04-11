from itertools import product

from odoo import models,fields,api

class DatePracticeWizard(models.TransientModel):
    # _inherit = "stock.quant"
    _name = "qty.update.wizard"
    _description = "On hand qty update wizard"

    location_id = fields.Many2one("stock.location",string="Warehouse Location")
    quantity = fields.Integer(string="Quantity")

    def update_on_hand_quantity(self):
        loc_id = self.location_id.id
        active_id = self.env.context.get('active_id')
        product_id = self.env['product.template'].browse(active_id)
        record = self.env['stock.quant'].search([('location_id','=',loc_id),('product_id','=',product_id.product_variant_id.id)])
        # record.write({'inventory_quantity_auto_apply':self.quantity})
        record.write({'inventory_quantity':self.quantity})
        record._apply_inventory()
