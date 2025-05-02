from odoo import fields,models,api

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    # account_move_line_id = fields.Many2one("sale.rma.line",string="RMA Line")