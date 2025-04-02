from odoo import models, fields, api
from odoo.exceptions import UserError


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
    move_ids = fields.One2many("stock.move","delivery_line_id",string="Delivery line")
    delivered_qty = fields.Integer(string="Delivered qty", compute='_compute_delivered_qty')


    @api.constrains('quantity')
    def check_quantity(self):
        for record in self:
            total_qty = sum(self.move_ids.mapped('product_uom_qty'))
            if record.quantity < total_qty:
                raise UserError("You can't change delivered quantity!")
        # record.delivered_qty = record.quantity
        # total_qty = sum(line.move_ids.mapped('product_uom_qty'))
        # remainning_qty = line.quantity - total_qty



    @api.onchange('product_id')
    def action_find_unit_price(self):
        if self.product_id:
            self.price_unit = self.product_id.lst_price

    @api.depends('quantity', 'price_unit')
    def action_count_total_price(self):
        for record in self:
            record.total_amount = record.price_unit * record.quantity

    @api.depends('move_ids.delivery_line_id')
    def _compute_delivered_qty(self):
        for record in self:
            record.delivered_qty = record.quantity


        # ready_state_delivery = self.env["stock.picking"].search([('state','=','ready'),('prescription_id','=',self.prescription_line_id.id)])
        # print(delivery_ready)
        # self.delivered_qty = 10
        # pass
        # for record in self:
        #     if record.product_id is rec.picking_id.product_id:
        #         record.delivered_qty = rec.picking_id.product_uom_qty
