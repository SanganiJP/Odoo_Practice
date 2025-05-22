from odoo import fields, models, api

class AccountInvoiceRecords(models.Model):
    _name = 'account.invoice.records'
    _description = 'Account Invoice Records'

    name = fields.Char(string="Invoice No")
    date = fields.Date(string="Date")
    due_amount = fields.Float(string="Due Amount")
    allocation_amount = fields.Float(string="Allocation Amount")
    payment_id = fields.Many2one("account.payment", string="Payment ID")