from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    so_order_approval = fields.Boolean(related='company_id.so_order_approval', string="Sale Order Approval", readonly=False)
    so_double_validation_amount = fields.Monetary(related='company_id.so_double_validation_amount', string="Minimum Amount", currency_field='company_currency_id',readonly=False)
