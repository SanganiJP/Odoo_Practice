from odoo import fields,models,api

class SaleRmaLines(models.Model):
    _name = "sale.rma.line"
    _description = "sale rma line model"

    product_id = fields.Many2one("product.product",string="Product")
    sale_order_qty = fields.Integer(string="SO Qty")
    unit_price = fields.Float(string="Unit Price")
    to_receive = fields.Integer(string="To Receive", compute="_compute_to_receive_qty", store=True)
    received_qty = fields.Integer(string="Receive Qty", compute="_compute_received_qty", store=True)
    available_qty = fields.Integer(string="Available Qty", compute="_compute_available_quantity", store=True)
    rma_id = fields.Many2one("sale.rma",string="Order ID")
    move_ids = fields.One2many("stock.move", "move_line_id", string="Delivery line")
    invoiced_qty = fields.Integer(string="Invoiced Qty", compute="_compute_invoiced_qty", store=True)
    invoice_line_ids = fields.One2many("account.move.line","account_move_line_id",string="invoice line")
    available_qty_to_invoice = fields.Integer(string="Available Qty To Invoice", compute="_compute_available_qty_to_invoice", store=True)

    @api.depends('move_ids.state','move_ids.product_uom_qty')
    def _compute_to_receive_qty(self):
        for rec in self:
            rec.to_receive = sum(rec.move_ids.filtered(lambda line : line.state not in ['cancel','draft','done']).mapped('product_uom_qty'))

    @api.depends('move_ids.state','move_ids.product_uom_qty')
    def _compute_received_qty(self):
        for rec in self:
            rec.received_qty = sum(rec.move_ids.filtered(lambda line : line.state in ['done']).mapped('quantity'))

    @api.depends('received_qty','sale_order_qty')
    def _compute_available_quantity(self):
        for rec in self:
            rec.available_qty = rec.sale_order_qty - rec.received_qty

    @api.depends('invoice_line_ids.parent_state')
    def _compute_invoiced_qty(self):
        for rec in self:
            rec.invoiced_qty = sum(rec.invoice_line_ids.filtered(lambda line : line.parent_state not in ['cancel']).mapped('quantity'))

    @api.depends('received_qty','invoiced_qty')
    def _compute_available_qty_to_invoice(self):
        for rec in self:
            rec.available_qty_to_invoice = rec.received_qty - rec.invoiced_qty
