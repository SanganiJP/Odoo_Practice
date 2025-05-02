from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    # @api.model_create_multi
    # def create(self, vals_list):
    #     res = super(SaleOrder, self).create(vals_list)
    #     for record in res:
    #         print(record)
    #     return res
    # self.order_line.purchase_line_ids.order_id

    def process_all(self):
        self.action_confirm()
        po = self._get_purchase_orders()
        if po:
            for order in po:
                po.button_confirm()
                for po_line in order.order_line:
                    for move in po_line.move_ids:
                        for so_line in self.order_line:
                            if so_line.product_id.id == move.product_id.id:
                                move.quantity = so_line.process_qty
                                break

                order.action_view_picking()
                data = order.picking_ids.button_validate()
                if data != True:
                    context = data.get('context')
                    picking = context.get('button_validate_picking_ids')
                    pickings_to_validate = self.env['stock.picking'].browse(picking).with_context(skip_backorder=True)
                    pickings_to_validate.button_validate()

                order.action_create_invoice()
                order.invoice_ids.invoice_date = fields.Date.today()
                order.invoice_ids.action_post()
                self.env['account.payment.register'].with_context(active_model='account.move',
                                                                  active_ids=order.invoice_ids.ids).create(
                    {'payment_date': fields.Date.today()}).action_create_payments()


        for line in self.order_line:
            for move in line.move_ids:
                move.quantity = line.process_qty

        data = self.picking_ids.button_validate()
        if data != True:
            context = data.get('context')
            picking = context.get('button_validate_picking_ids')
            pickings_to_validate = self.env['stock.picking'].browse(picking).with_context(skip_backorder=True)
            pickings_to_validate.button_validate()
        self.picking_ids.button_validate()
        self._create_invoices()
        self.invoice_ids.action_post()
        self.env['account.payment.register'].with_context(active_model='account.move',
                                                          active_ids=self.invoice_ids.ids).create(
            {'payment_date': fields.Date.today()}).action_create_payments()

# po = self._get_purchase_orders()
#
# if po:
#     po.button_confirm()
#     po.action_view_picking()
#     po.picking_ids.button_validate()
#     po.action_create_invoice()
#     po.invoice_ids.invoice_date = '2025-05-01'
#     po.invoice_ids.action_post()
#     self.env['account.payment.register'].with_context(active_model='account.move', active_ids=po.invoice_ids.ids).create({'payment_date': '2025-05-01'}).action_create_payments()
#
# self.picking_ids.button_validate()
# self._create_invoices()
# self.invoice_ids.action_post()
# self.env['account.payment.register'].with_context(active_model='account.move', active_ids=self.invoice_ids.ids).create({'payment_date': '2025-05-01'}).action_create_payments()
