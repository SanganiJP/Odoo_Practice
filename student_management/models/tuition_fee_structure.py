# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TuitionFeeStructure(models.Model):
    _name = 'tuition.fee.structure'
    _description = 'student_management.tuition.fee.structure'
    _rec_name = 'course_name'

    course_name = fields.Many2one("product.template", string="Course", domain=[('type', '=', 'service')])
    course_fee_amount = fields.Float(string="Course Price")
    quantity = fields.Float(string="Quantity", default="1.0")
    discount = fields.Float(string="Discount(%)")
    course_fees = fields.Float(string="Total Fees", compute="_compute_subtotal", store=True)
    total = fields.Float(string="Fees to pay", compute="_compute_total", store=True)
    standard = fields.Selection(
        [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'),
         ('10', '10'), ('11', '11'), ('12', '12')],
        string="Standard", default='1')

    @api.onchange('course_name')
    def get_course_fee_amount(self):
        for rec in self:
            if rec.course_name:
                rec.course_fee_amount = self.course_name.list_price
        # self.write({
        #     'course_fee_amount': self.course_name.list_price
        # })

    @api.depends('quantity', 'course_fee_amount')
    def _compute_subtotal(self):
        for rec in self:
            if rec.quantity and rec.course_fee_amount:
                rec.course_fees = rec.quantity * rec.course_fee_amount

    @api.depends('course_fees', 'discount')
    def _compute_total(self):
        for rec in self:
            if rec.course_fees and rec.discount:
                rec.total = rec.course_fees - ((rec.course_fees * rec.discount) / 100)


