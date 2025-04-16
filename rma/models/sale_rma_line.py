from odoo import fields,models,api

class SaleRmaLines(models.Model):
    _name = "sale.rma.line"
    _description = "sale rma line model"

    product_id = fields.Many2one("product.product",string="Product")
    sale_order_qty = fields.Integer(string="SO Qty")
    unit_price = fields.Float(string="Unit Price")
    # to_receive = fields.Integer(string="To Receive")
    to_receive = fields.Integer(string="To Receive", compute="_compute_to_receive_qty")
    received_qty = fields.Integer(string="Receive Qty", compute="_compute_received_qty")
    rma_id = fields.Many2one("sale.rma",string="Order ID")
    move_ids = fields.One2many("stock.move", "move_line_id", string="Delivery line")

    @api.depends('move_ids.state')
    def _compute_to_receive_qty(self):
        for rec in self:
            record = self.env['stock.move'].search([('move_line_id', '=', rec.id)])
            rec.to_receive = record.quantity

    @api.depends('move_ids.state')
    def _compute_received_qty(self):
        for rec in self:
            record = self.env['stock.move'].search([('move_line_id', '=', rec.id)])
            rec.received_qty = record.quantity