from wheel.metadata import _

from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    state = fields.Selection(selection_add=[('to_approve', 'To approve'), ('sale',)])
    service_type_product_qty = fields.Integer(string="Service Product Qty", compute="_compute_service_type_product_qty",
                                              store=True)

    def _approval_allowed(self):
        """Returns whether the order qualifies to be approved by the current user"""
        self.ensure_one()
        amount = self.env['ir.config_parameter'].sudo().get_param('Amount')

        if self.env['ir.config_parameter'].sudo().get_param('Approval'):
            return (self.amount_total < float(amount)
                    or self.env.user.has_group('practical_jayesh.group_sale_approver'))
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

    def button_cancel(self):
        pass

    @api.depends('order_line.product_id')
    def _compute_service_type_product_qty(self):
        for rec in self:
            rec.service_type_product_qty = len(rec.order_line.filtered(lambda line: line.product_id.type == 'service'))

            # rec.service_type_product_qty = sum(
            #     rec.order_line.filtered(lambda line: line.product_id.type == 'service').mapped('product_uom_qty'))

    def action_add_product_wizard(self):
        view_id = self.env.ref('practical_jayesh.add_product_wizard_form').id
        return {
            'name': 'Add Product',
            'view_mode': 'form',
            'res_model': 'add.product.wizard',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
