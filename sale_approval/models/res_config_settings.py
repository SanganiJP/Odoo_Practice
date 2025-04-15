from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    so_order_approval = fields.Boolean("Sale Order Approval", default=lambda self: self.env.company.po_double_validation == 'two_step')
    so_double_validation = fields.Selection(related='company_id.so_double_validation', string="Levels of Approvals *", readonly=False)
    so_double_validation_amount = fields.Monetary(related='company_id.so_double_validation_amount', string="Minimum Amount", readonly=False)
