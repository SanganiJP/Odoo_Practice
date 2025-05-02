import typing

from odoo import fields, models, api
from odoo.api import ValuesType
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    process_qty = fields.Integer(string="Process Qty")

    @api.onchange('process_qty')
    def check_process_qty(self):
        if self.process_qty > self.product_uom_qty:
            raise UserError('Process Quantity should be less or equal then Quantity!')

    # def write(self, vals):
    #     res = super(SaleOrderLine,self).write(vals)
    #     if self.move_ids.state not in ['done','cancel']:
    #         self.move_ids.quantity = self.process_qty
    #     return res
