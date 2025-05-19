from odoo import models, fields, api
from odoo.exceptions import ValidationError


class MoComponentSerialProduct(models.TransientModel):
    _name = "mo.component.serial.product"
    _description = "Mo Component serial Product"

    mo_number = fields.Char(string="Mo No.")
    product_code = fields.Char(string="Product")
    old_serial = fields.Char(string="Old serial no")
    new_serial = fields.Char(string="New serial no")
    mo_product_id = fields.Many2one("update.mrp.component.wizard", string="Product")

