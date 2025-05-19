from odoo import models, fields, api
from odoo.exceptions import ValidationError


class MoComponentData(models.TransientModel):
    _name = "mo.component.data"
    _description = "Mo Component Data Wizard"

    mo_number = fields.Char(string="Mo No.")
    current_product = fields.Many2one("product.product", string="Current Product")
    new_product = fields.Many2one("product.product", string="New Product")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('progress', 'In Progress'),
        ('to_close', 'To Close'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')] ,string="Mo State")
    mo_product_id = fields.Many2one("update.mrp.component.wizard", string="Product")
