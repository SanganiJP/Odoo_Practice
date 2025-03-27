from odoo import fields, models, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    extra_discount = fields.Integer(string="Extra Discount")