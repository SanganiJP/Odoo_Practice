from odoo import models, fields, api


class PrescriptionLine(models.Model):
    _name = "prescription.line"
    _description = "Prescription line model"
    _rec_name = 'product_id'

    # name = fields.Char(string="Name")
    product_id = fields.Many2one("product.product", string="Product Name")
    quantity = fields.Integer(string="Quantity", default=1)
    price_unit = fields.Float(string="Price")
    total_amount = fields.Float(default=0, compute='action_count_total_price', string="Total amount", store=True)
    prescription_line_id = fields.Many2one("hms.prescription", string="My Prescription")

    @api.onchange('product_id')
    def action_find_unit_price(self):
        if self.product_id:
            self.price_unit = self.product_id.lst_price

    @api.depends('quantity', 'price_unit')
    def action_count_total_price(self):
        for record in self:
            record.total_amount = record.price_unit * record.quantity
