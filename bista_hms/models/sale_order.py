from odoo import fields,models,api
from num2words import num2words

class SaleOrder(models.Model):
    _inherit = "sale.order"

    extra_note = fields.Text(string="Extra Note")
    discount_amount = fields.Float(string="Discount Amount")
    total_amount = fields.Float(string="Total Amount", compute='_compute_total_amount', store=True)
    lead_reference = fields.Char(string="Lead Reference")
    total_amount_in_word = fields.Char(string="Total Amount(In Words)",  compute='_compute_total_amount_in_words')

    @api.depends('discount_amount','total_amount')
    def _compute_total_amount(self):
        for record in self:
            order_line = self.env['sale.order.line'].search([('order_id','=',record.id)])
            record.total_amount = sum(order_line.mapped('price_subtotal')) - record.discount_amount

    @api.onchange('partner_id')
    def check_customer_tc(self):
        for rec in self:
            if rec.partner_id.use_customers_tc:
                rec.note = rec.partner_id.terms_and_conditions

    def _compute_total_amount_in_words(self):
        for rec in self:
            rec.total_amount_in_word = num2words(rec.amount_total, lang='en', to="currency", currency="INR" ).title()

    def calculate_discount_amount(self):
        # order_line = self.env['sale.order.line'].search([('order_id','=',self.id)])
        discount = 0
        for line in self.order_line:
            discount += (((line.product_uom_qty * line.price_unit) * line.discount) / 100)
        return discount
