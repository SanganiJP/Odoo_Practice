from datetime import date
from odoo import fields, models, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError

class LoanSystem(models.Model):
    _name = 'loan.system'
    _description = 'Description'
    _rec_name = 'partner_id'

    partner_id = fields.Many2one("res.partner", string="Customer")
    loan_amount = fields.Float("Loan Amount")
    period_tenure = fields.Integer(string="Period Tenure", default=1)
    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date")
    emi_date = fields.Date(string="EMI Date", required=True)
    emi_amount = fields.Float(compute='_compute_emi_amount', string="EMI Amount", store=True)
    total_interest_amount = fields.Float(compute='_compute_total_interest_amount', string="Total Interest Amount ", store=True)
    total_amount = fields.Float(compute='_compute_total_amount', string="Total Amount", store=True)
    emi_line_ids = fields.One2many("emi.lines", "loan_id")
    interest_rate_ids = fields.One2many("loan.interest.rate", "loan_id")
    current_interest_rate = fields.Float(string="Current Interest Rate")
    invoice_count = fields.Integer(compute='_compute_invoice_count', default=0, store=True)
    invoice_ids = fields.One2many('account.move', 'loan_id')

    @api.onchange('start_date', 'period_tenure')
    def onchange_end_date(self):
        if self.start_date:
            self.end_date = self.start_date + relativedelta(months=self.period_tenure)

    @api.depends('loan_amount', 'period_tenure')
    def _compute_emi_amount(self):
        for rec in self:
            if rec.loan_amount and rec.period_tenure:
                ir = rec.interest_rate_ids.filtered(lambda line: line.is_active == True).interest_rate
                # self.current_interest_rate = ir
                if ir:
                    rate = (ir / 12) / 100
                    rec.emi_amount = round((rec.loan_amount * rate * pow(1 + rate, rec.period_tenure)) / (
                            pow(1 + rate, rec.period_tenure) - 1))

    @api.depends('period_tenure', 'loan_amount', 'emi_amount')
    def _compute_total_interest_amount(self):
        for rec in self:
            if rec.emi_amount:
                rec.total_interest_amount = round(rec.emi_amount * rec.period_tenure - rec.loan_amount)

    @api.depends('period_tenure', 'emi_amount')
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = round(rec.emi_amount * rec.period_tenure)

    def generate_emi_lines(self):
        emi_line_record_list = []
        emi_date = self.emi_date
        emi_amount = self.emi_amount
        remaining_principal = self.loan_amount

        ir = self.interest_rate_ids.filtered(lambda line: line.is_active == True).interest_rate
        monthly_interest_rate = (ir / 12) / 100

        for month in range(self.period_tenure):
            interest = round(remaining_principal * monthly_interest_rate)
            principal_paid = emi_amount - interest
            remaining_principal = remaining_principal - principal_paid
            emi_line_vals = {
                'emi_date': emi_date,
                'principal_paid': principal_paid,
                'interest_charged': interest,
                'total_payment': emi_amount,
                'balance': remaining_principal,
                'loan_id': self.id,
            }
            emi_line_record_id = self.env['emi.lines'].create(emi_line_vals)
            emi_line_record_list.append(emi_line_record_id.id)
            emi_date = emi_date + relativedelta(months=1)

        self.emi_line_ids = [(6, 0, emi_line_record_list)]

    def action_view_invoice(self):
        form_view_id = self.env.ref('account.view_move_form').id
        list_view_id = self.env.ref('account.view_out_invoice_tree').id

        res = {
            'name': 'Invoices',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'account.move',
            'views': [(list_view_id, 'list'), (form_view_id, 'form')],
            'target': 'current',
            'domain': [('loan_id', '=', self.id)],
        }

        return res

    @api.depends('invoice_ids')
    def _compute_invoice_count(self):
        for rec in self:
            rec.invoice_count = self.env['account.move'].search_count([('loan_id', '=', rec.id)])

    def generate_emi_invoice(self):
        today = date.today()
        # loan_record = self.env['loan.system'].search([('')])
        todays_emi = self.env['emi.lines'].search([
            ('emi_date', '=', today)
        ])
        product_id = self.env['product.product'].search([('name', '=', 'emi')]).id
        for rec in todays_emi:
            move_vals = {
                'move_type': 'out_invoice',
                'invoice_date': rec.emi_date,
                'partner_id': rec.loan_id.partner_id.id,
                'partner_shipping_id': rec.loan_id.partner_id.id,
                'loan_id': rec.loan_id.id,
            }
            invoice = self.env['account.move'].create(move_vals)

            move_line_vals = {
                'product_id': product_id,
                'quantity': 1,
                'move_id': invoice.id,
                'price_unit': rec.total_payment,
            }
            self.env['account.move.line'].create(move_line_vals)
            rec.state = 'invoiced'
            invoice.action_post()
            if rec.loan_id.partner_id.email:
                template_id = self.env.ref('bista_loan.emi_payment_request_email_template')
                template_id.send_mail(rec.loan_id.id, force_send=True)



    # def invoice_payment(self):
    #     invoices = self.env['account.move'].search([('state', '=', 'invoiced')])
    #     for invoice in invoices:
    #         self.env['account.payment.register'].with_context(active_model='account.move').create({'payment_date': fields.Date.today()}).action_create_payments()


































































    # def generate_emi_lines(self):
    #     emi_date = self.emi_date
    #     emi_amount = self.emi_amount
    #     remaining_principal = self.loan_amount
    #
    #     ir = self.interest_rate_ids.filtered(lambda line: line.is_active == True).interest_rate
    #     monthly_interest_rate = (ir / 1200)
    #
    #     self.emi_line_ids = [(5,0,0)]
    #
    #     for month in range(self.period_tenure):
    #         interest = round(remaining_principal * monthly_interest_rate)
    #         principal_paid = round(emi_amount - interest)
    #         remaining_principal = round(remaining_principal - emi_amount)
    #         self.env['emi.lines'].create({
    #             'emi_date': emi_date,
    #             'principal_paid': principal_paid,
    #             'interest_charged': interest,
    #             'total_payment' : emi_amount,
    #             'loan_id': self.id,
    #             'balance' : remaining_principal
    #         })
    #
    #         print(f"Month === {month}",remaining_principal)
    #         emi_date += relativedelta(months=1)
