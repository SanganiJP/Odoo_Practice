from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sale_approval = fields.Boolean(string="Sale Order Approval", config_parameter="Approval", readonly=False)
    sale_min_amount = fields.Float(string="Minimum Amount",config_parameter="Amount", readonly=False)