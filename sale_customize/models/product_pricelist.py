# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import UserError


class Pricelist(models.Model):
    _inherit = "product.pricelist"

    is_active = fields.Boolean(string="Activate As special Pricelist", default=False)

    @api.onchange('is_active')
    def onchange_is_active(self):
        if self.name:
            active_pricelist =self.env['product.pricelist'].search([('is_active','=',True)])
            if active_pricelist:
                if not active_pricelist.name == self.name:
                    raise UserError('One special price list is already active!')
            else:
                self.is_active = True