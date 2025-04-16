from wheel.metadata import _

from odoo import fields,models,api

class SaleOrder(models.Model):
    _inherit = "sale.order"

    state = fields.Selection(selection_add=[('to_approve', 'To approve'),('sale',)])

    def _approval_allowed(self):
        """Returns whether the order qualifies to be approved by the current user"""
        self.ensure_one()
        if self.env.user.company_id.so_order_approval:
            return (self.amount_total < self.env.company.currency_id._convert(
                        self.company_id.so_double_validation_amount, self.currency_id, self.company_id,
                        self.date_order or fields.Date.today())
                    or self.env.user.has_group('sales_team.group_sale_manager'))
        else:
            return True

    def button_approve(self, force=False):
        self.with_context(Approve=True).action_confirm()

    def _confirmation_error_message(self):
        """ Return whether order can be confirmed or not if not then returm error message. """
        self.ensure_one()
        if self.state not in {'draft', 'sent', 'to_approve'}:
            return _("Some orders are not in a state requiring confirmation.")
        if any(
            not line.display_type
            and not line.is_downpayment
            and not line.product_id
            for line in self.order_line
        ):
            return _("A line on these orders missing a product, you cannot confirm it.")

        return False

    def action_confirm(self):
        if self._context.get("Approve"):
            return super(SaleOrder, self).action_confirm()
        else:
            for order in self:
                if order.state not in ['draft', 'sent', 'to_approve']:
                    continue
                if order._approval_allowed():
                    order.button_approve()
                else:
                    order.write({'state': 'to_approve'})
