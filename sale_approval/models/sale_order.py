from odoo import fields,models,api

class SaleOrder(models.Model):
    _inherit = "sale.order"

    state = fields.Selection(selection_add=[('to_approve', 'To approve'),('sent',)])

    def _approval_allowed(self):
        """Returns whether the order qualifies to be approved by the current user"""
        self.ensure_one()
        return (
                self.company_id.so_double_validation == 'one_step'
                or (self.company_id.so_double_validation == 'two_step'
                    and self.amount_total < self.env.company.currency_id._convert(
                    self.company_id.so_double_validation_amount, self.currency_id, self.company_id,
                    ))
                or self.env.user.has_group('sales_team.group_sale_manager'))

    def button_approve(self, force=False):
        self = self.filtered(lambda order: order._approval_allowed())
        self.write({'state': 'sale'})
        # self.filtered(lambda p: p.company_id.po_lock == 'lock').write({'state': 'done'})
        return {}

    def action_confirm(self):
        for order in self:
            # if order.state not in ['draft', 'sent']:
            #     continue
            # order.order_line._validate_analytic_distribution()
            # order._add_supplier_to_product()
            # Deal with double validation process
            if order._approval_allowed():
                order.button_approve()
            else:
                order.write({'state': 'to_approve'})
            # if order.partner_id not in order.message_partner_ids:
            #     order.message_subscribe([order.partner_id.id])
        return True

