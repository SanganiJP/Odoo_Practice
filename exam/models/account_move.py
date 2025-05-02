from odoo import fields,models,api

class AccountMove(models.Model):
    _inherit = "account.move"

    # rma_invoice_id = fields.Many2one("sale.rma",string="Invoice")