# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class Company(models.Model):
    _inherit = 'res.company'

    so_order_approval = fields.Boolean()

    so_double_validation_amount = fields.Monetary(string='Double validation amount', default=5000,
        help="Minimum amount for which a double validation is required")

    quote_notification_before_expiry = fields.Integer(string="Default Quotation Validity", default=30)
