from datetime import date
from odoo import fields, models, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo.fields import Datetime

STATUS = [('draft', 'Draft'),
          ('to_approve', 'To Approve'),
          ('rejected', 'Rejected'),
          ('approved', 'Approved')]


class LoanSystem(models.Model):
    _name = 'loan.system'
    _description = 'Description'

    name = fields.Char(string="Loan No", copy=False, readonly=True, index=True, default="New")
    partner_id = fields.Many2one("res.partner", string="Customer", copy=False)
    loan_amount = fields.Float(string="Loan Amount", copy=False)
    period_tenure = fields.Integer(string="Period Tenure", copy=False)
    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date")
    emi_date = fields.Date(string="EMI Date", required=True)
    emi_amount = fields.Float(compute='_compute_emi_amount', string="EMI Amount", store=True)
    total_interest_amount = fields.Float(compute='_compute_total_interest_amount', string="Total Interest Amount ",
                                         store=True)
    total_principle_amount = fields.Float(compute='_compute_total_principle_amount', string="Total Principal Amount",
                                          store=True)
    emi_line_ids = fields.One2many("emi.lines", "loan_id")
    interest_rate_ids = fields.One2many("loan.interest.rate", "loan_id")
    current_interest_rate = fields.Float(string="Current Interest Rate", copy=False)
    invoice_count = fields.Integer(compute='_compute_invoice_count', default=0, store=True)
    invoice_ids = fields.One2many('account.move', 'loan_id')
    next_emi_date = fields.Date(compute='_compute_next_emi_date', string="Next EMI Date", store=True)
    paid_principle_amount = fields.Float(string='paid Principle amount')
    loan_stage = fields.Selection(STATUS, string="Stage", default='draft', copy=False)
    team_id = fields.Many2one("loan.approval.team", string="Team")
    loan_approval_level_ids = fields.One2many("loan.approval.level", "loan_id")
    # next_approver = fields.Many2many('res.users', compute='_compute_next_approver', string="Next Approver")
    next_approver = fields.Many2many('res.users', string="Next Approver")
    current_user = fields.Many2one('res.users', compute='_compute_current_user', string="Current Loan System User")
    assign_user_ids = fields.Many2many('res.users', "rel_res_users", column1="loan_id", column2="res_users_id", string="Assign To")

    @api.model_create_multi
    def create(self, val_list):
        res = super(LoanSystem, self).create(val_list)
        for record in res:
            record.name = self.env["ir.sequence"].next_by_code('loan.system')
        return res

    def _compute_current_user(self):
        self.current_user = self.env.user.id

    # def _compute_next_approver(self):
    #     for rec in self:
    #         rec.next_approver = rec.loan_approval_level_ids.filtered(
    #             lambda level: level.loan_approve_stage == 'to_approve').team_member.ids

    @api.onchange('team_id')
    def onchange_team_id(self):
        if self.team_id:
            self.loan_approval_level_ids = [(5,0,0)]
            lst = []
            # levels = self.env['approval.levels'].search([('team_id', '=', self.team_id.id)])
            for level in self.team_id.approval_level_ids:
                lst.append((0, 0, {
                    'name': level.name,
                    'team_level': level.team_level,
                    'team_member': level.team_member.ids,
                }))
            self.loan_approval_level_ids = lst
            self.loan_approval_level_ids[0].loan_approve_stage = 'to_approve'
            self.next_approver = self.loan_approval_level_ids.filtered(lambda level: level.loan_approve_stage == 'to_approve').team_member.ids
            self.assign_user_ids = self.loan_approval_level_ids.filtered(lambda level: level.loan_approve_stage == 'to_approve').team_member.ids

    def action_confirm(self):
        self.loan_stage = 'to_approve'
        # self.loan_approval_level_ids[0].loan_approve_stage = 'to_approve'

    def action_reject(self):
        approval_level = self.loan_approval_level_ids.filtered(lambda level: level.loan_approve_stage == 'to_approve')
        if approval_level:
            approval_level.loan_approve_stage = 'rejected'
            approval_level.rejected_by = self.current_user
            approval_level.approve_time = Datetime.today()
            self.loan_stage = 'rejected'

    def action_approve(self):
        approval_level = self.loan_approval_level_ids.filtered(lambda level: level.loan_approve_stage == 'to_approve')
        if approval_level:
            approval_level.loan_approve_stage = 'approved'
            approval_level.approved_by = self.current_user
            approval_level.approve_time = Datetime.today()

        pending_approval_level = self.loan_approval_level_ids.filtered(lambda level: level.loan_approve_stage == 'pending')
        if pending_approval_level:
            pending_approval_level[0].loan_approve_stage = 'to_approve'
            self.next_approver = pending_approval_level[0].team_member.ids
            self.assign_user_ids = pending_approval_level[0].team_member.ids

        if not approval_level:
            self.loan_stage = 'approved'


    @api.depends('emi_line_ids.state', 'emi_date')
    def _compute_next_emi_date(self):
        for rec in self:
            emi_rec = rec.emi_line_ids.filtered(lambda line: line.state == 'pending')
            if emi_rec:
                rec.next_emi_date = emi_rec[0].emi_date
            else:
                rec.next_emi_date = rec.emi_date

    @api.onchange('start_date', 'period_tenure')
    def onchange_end_date(self):
        if self.start_date:
            self.end_date = self.start_date + relativedelta(months=self.period_tenure)

    @api.depends('loan_amount', 'period_tenure', 'current_interest_rate')
    def _compute_emi_amount(self):
        for rec in self:
            if rec.loan_amount and rec.period_tenure:
                month_interest_rate = (self.current_interest_rate / 1200)
                pending_emi_lines = self.emi_line_ids.filtered(lambda line: line.state == 'pending')
                # if pending_emi_lines :
                self.emi_line_ids.filtered(lambda line: line.state == 'pending').unlink()
                new_period_tenure = rec.period_tenure - len(self.emi_line_ids)
                new_loan_amount = rec.loan_amount - sum(
                    rec.emi_line_ids.filtered(lambda line: line.state != 'pending').mapped('total_payment'))
                if self.current_interest_rate and new_period_tenure:
                    rec.emi_amount = round(
                        (new_loan_amount * month_interest_rate * pow(1 + month_interest_rate, new_period_tenure))
                        / (pow(1 + month_interest_rate, new_period_tenure) - 1))

    @api.depends('emi_amount', 'emi_line_ids')
    def _compute_total_interest_amount(self):
        for rec in self:
            if rec.emi_amount:
                rec.total_interest_amount = round((rec.emi_amount * rec.period_tenure - rec.loan_amount) + sum(
                    rec.emi_line_ids.filtered(lambda line: line.state != 'pending').mapped('interest_charged')))

    @api.depends('total_interest_amount')
    def _compute_total_principle_amount(self):
        for rec in self:
            if rec.total_interest_amount:
                rec.total_principle_amount = rec.loan_amount + rec.total_interest_amount

    @api.depends('invoice_ids')
    def _compute_invoice_count(self):
        for rec in self:
            # rec.invoice_count = self.env['account.move'].search_count([('loan_id', '=', rec.id)])
            rec.invoice_count = len(rec.invoice_ids)

    def generate_emi_lines(self):
        emi_line_record = []
        emi_date = self.emi_date
        emi_amount = self.emi_amount
        remaining_principal = self.loan_amount

        # ir = self.interest_rate_ids.filtered(lambda line: line.is_active == True).interest_rate
        monthly_interest_rate = (self.current_interest_rate / 12) / 100

        # pending_emi_record = self.emi_line_ids.filtered(lambda line: line.state == 'pending')
        # pending_emi_record.unlink()
        # emi_line_record += self.emi_line_ids
        emi_date = emi_date + relativedelta(months=len(self.emi_line_ids))
        remaining_principal -= sum(
            self.emi_line_ids.filtered(lambda line: line.state != 'pending').mapped('total_payment'))

        for month in range(self.period_tenure - len(self.emi_line_ids)):
            interest = round(remaining_principal * monthly_interest_rate)
            principal_amount = emi_amount - interest
            # total_payment = principal_amount + interest
            remaining_principal = remaining_principal - principal_amount
            vals = (0, 0, {
                'emi_date': emi_date,
                'principal_amount': principal_amount,
                'interest_charged': interest,
                'total_payment': emi_amount,
                'balance': remaining_principal,
            })
            emi_line_record.append(vals)
            emi_date = emi_date + relativedelta(months=1)
        self.emi_line_ids = emi_line_record

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

    def action_generate_emi_invoice(self):
        today = date.today()
        todays_emi = self.env['emi.lines'].search([
            ('emi_date', '=', today),
            ('loan_id.loan_stage', '=', 'approved')
        ])
        product_id = self.env.ref('bista_loan.product_loan_emi').id
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
            # if rec.loan_id.partner_id.email:
            #     template_id = self.env.ref('bista_loan.emi_payment_request_email_template')
            #     template_id.send_mail(rec.loan_id.id, force_send=True)
