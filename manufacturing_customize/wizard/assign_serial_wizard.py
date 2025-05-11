from odoo import models, fields, api
from odoo.exceptions import UserError


class AssignSerialWizard(models.TransientModel):
    _name = "assign.serial.wizard"
    _description = "description"

    number_of_serial_no = fields.Integer(string="Number Of SN")

    def assign_serial(self):
        ticket_id = self.env.context.get('active_id')
        if ticket_id:
            record = self.env['mrp.production'].browse(ticket_id)
            for rec in range(self.number_of_serial_no):
                seq = record.product_id.sequence_id.next_by_code('product.product')
                serial_record = {
                    'name': seq,
                    'product_id': record.product_id.id,
                }
                serial_numbers_id = self.env['stock.lot'].create([serial_record])
                record.lot_ids = [(4,serial_numbers_id.id)]

    @api.onchange('number_of_serial_no')
    def check_number_of_serial_no(self):
        ticket_id = self.env.context.get('active_id')
        if ticket_id:
            record = self.env['mrp.production'].browse(ticket_id)
            if (record.product_qty - len(record.lot_ids)) < self.number_of_serial_no:
                raise UserError("You can not generate more serial number then product Quantity!")
            if self.number_of_serial_no < 0:
                raise UserError("Entered number should be positive number!")


