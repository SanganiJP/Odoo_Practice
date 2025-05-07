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

    # def assign_serial(self):
    #     ticket_id = self.env.context.get('active_id')
    #     if ticket_id:
    #         record = self.env['mrp.production'].browse(ticket_id)
    #         for rec in range(self.number_of_serial_no):
    #             seq = record.product_id.sequence_id.next_by_code('product.product')
    #             serial_record = {
    #                 'name': seq,
    #                 'product_id': record.product_id.id,
    #             }
    #             serial_numbers_id = self.env['stock.lot'].create([serial_record])
    #             record.lot_ids = [(4,serial_numbers_id.id)]

    def process_all(self):
        self.action_confirm()
        po = self._get_purchase_orders()
        if po:
            for order in po:
                po.button_confirm()
                for po_line in order.order_line:
                    for move in po_line.move_ids:
                        if move.product_id.sequence_id:
                            for rec in range(int(move.quantity)):
                                # seq = order.picking_ids.move_ids.product_id.sequence_id.next_by_code('product.product')
                                seq = move.product_id.sequence_id.next_by_id()
                                serial_record = {
                                    'name': seq,
                                    'product_id': move.product_id.id,
                                }
                                serial_numbers_id = self.env['stock.lot'].create([serial_record])
                                move.lot_ids = [(4, serial_numbers_id.id)]
                        for so_line in self.order_line:
                            if so_line.product_id.id == move.product_id.id:
                                move.quantity = so_line.process_qty
                                break

                order.action_view_picking()

                # if order.picking_ids.move_ids.product_id.sequence_id:
                #     for rec in range(int(order.picking_ids.move_ids.quantity)):
                #         # seq = order.picking_ids.move_ids.product_id.sequence_id.next_by_code('product.product')
                #         seq = order.picking_ids.move_ids.product_id.sequence_id.next_by_id()
                #         serial_record = {
                #             'name': seq,
                #             'product_id': order.picking_ids.move_ids.product_id.id,
                #         }
                #         serial_numbers_id = self.env['stock.lot'].create([serial_record])
                #         order.picking_ids.move_ids.lot_ids = [(4, serial_numbers_id.id)]

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
        # self.picking_ids.button_validate()
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
