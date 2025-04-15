from odoo import models,fields,api
from odoo.exceptions import UserError


class RmaLineWizard(models.TransientModel):
    _name = "rma.wizard"
    _description = "qty update wizard"

    ticket_id = fields.Many2one("sale.rma",string="Record ID")
    wizard_rma_lines_ids = fields.One2many("wizard.rma.lines","wizard_rma_line_id", string=" ")


    def process_return(self):
        delivery_vals = self.prepare_delivery_vals()
        delivery_id = self.env['stock.picking'].create(delivery_vals)

        delivery_line_vals = self.prepare_delivery_line_vals(delivery_id)
        self.env['stock.move'].create(delivery_line_vals)

        if not delivery_line_vals:
            delivery_id.unlink()
            raise UserError('Please add product to deliver!')

        delivery_id.action_confirm()

    def prepare_delivery_vals(self):
        picking_type_id = self.env['stock.picking.type'].search([('code', '=', 'incoming')], limit=1)
        self.ticket_id = self.env.context.get('active_id')
        values = {
            'partner_id': self.ticket_id.sale_order_id.partner_id.id,
            'origin': self.ticket_id.sale_order_id.name,
            'location_id': picking_type_id.default_location_src_id.id,
            'location_dest_id': picking_type_id.default_location_dest_id.id,
            'picking_type_id': picking_type_id.id,
            'picking_id': self.ticket_id.id,
        }
        return values

    def prepare_delivery_line_vals(self, delivery_id):
        move_vals = []
        for line in self.wizard_rma_lines_ids:
            if line.qty > 0:
                vals = {
                    'name': line.product_id.display_name,
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.qty,
                    'location_id': delivery_id.location_id.id,
                    'location_dest_id': delivery_id.location_dest_id.id,
                    'picking_id': delivery_id.id,
                    'picking_type_id': delivery_id.picking_type_id.id,
                    'move_line_id': line.rma_lines_id.id,
                }
                move_vals.append(vals)
        return move_vals

    @api.onchange('ticket_id')
    def onchange_sale_order(self):
        self.ticket_id = self.env.context.get('active_id')
        if self.ticket_id:
            records = self.env['sale.rma'].browse(self.ticket_id.id)
            rma_lines = []
            for line in records.rma_line_ids:
                rma_lines.append((0, 0, {
                    'product_id': line.product_id.id,
                    'so_qty': line.sale_order_qty,
                    'qty': line.sale_order_qty,
                    'rma_lines_id': line.id,
                }))
            self.wizard_rma_lines_ids = rma_lines
