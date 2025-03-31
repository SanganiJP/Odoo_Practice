from odoo import fields,models,api

class SaleOrder(models.Model):
    _inherit = "sale.order"

    note = fields.Text(string="Extra Note")
    discount_amount = fields.Float(string="Discount Amount")
    total_amount = fields.Float(string="Total Amount", compute='_compute_total_amount', store=True)
    lead_reference = fields.Char(string="Lead Reference")

    @api.depends('discount_amount','total_amount')
    def _compute_total_amount(self):
        for record in self:
            order_line = self.env['sale.order.line'].search([('order_id','=',record.id)])
            record.total_amount = sum(order_line.mapped('price_subtotal')) - record.discount_amount
