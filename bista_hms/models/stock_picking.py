from odoo import fields,models,api

class StockPicking(models.Model):
    _inherit = "stock.picking"

    lead_reference = fields.Char(string="Lead Reference")
    prescription_id = fields.Many2one("hms.prescription",string="Prescription")
