from datetime import date, timedelta

from odoo import models, fields, api
from odoo.exceptions import UserError


class HmsPrescription(models.Model):
    _name = "hms.prescription"
    _description = "hms prescription"
    _rec_name = "patient_id"

    prescription_code = fields.Char(string="Prescription ID", default="New")
    patient_id = fields.Many2one("res.patient", string="Patient Name", required=True)
    prescription_date = fields.Date(string="Prescription Date", default=date.today())
    prescription_lines = fields.One2many("prescription.line", "prescription_line_id", string="Prescription")
    lead_reference = fields.Char(string="Lead Reference")
    state = fields.Selection([('draft', 'Draft'),
                              ('confirm', 'Confirmed'),
                              ('ready', 'Ready'),
                              ('done','Done'),
                              ('cancel', 'Cancelled')],
                             string="Status", default='draft')
    delivery_ids = fields.One2many("stock.picking","prescription_id",string="Deliveries")
    delivery_count = fields.Integer(default=0, compute='_compute_count_delivery')

    @api.model_create_multi
    def create(self, val_list):
        res = super(HmsPrescription, self).create(val_list)
        for record in res:
            record.prescription_code = self.env["ir.sequence"].next_by_code('hms.prescription')
        return res

    def action_confirm(self):
        self.state = 'confirm'

    def action_cancel(self):
        self.state = 'cancel'

    def _create_weekly_prescription_report(self):
        week_report = []
        start_of_week = date.today() - timedelta(days=7)
        end_of_week = date.today()
        diff = end_of_week - start_of_week
        print(diff.days)

        prescriptions = self.env["hms.prescription"].search([
            ('prescription_date', '>', start_of_week),
            ('prescription_date', '<=', end_of_week),
        ])

        for prescription in prescriptions:
            report = {}
            report.update({'Prescription code' : prescription.prescription_code, 'Patient Name' : prescription.patient_id.name,'Prescription date':prescription.prescription_date})
            week_report.append(report)

        print(week_report)

    def action_prescription_line(self):
        list_id = self.env.ref('bista_hms.prescription_line_list_view').id
        form_id = self.env.ref('bista_hms.prescription_line_from_view').id

        return {
            'name': 'Prescription',
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'res_model': 'prescription.line',
            # 'view_id': view_id,
            'views': [(list_id,'list'),(form_id,'form')],
            'target': 'current',
            'domain' : [('prescription_line_id', '=', self.id)]
            # 'context': {'default_patient_id': self.id}
        }

    def action_create_prescription_invoice(self):
        invoice_vals = self.prepare_invoice()
        invoice_id = self.env['account.move'].create(invoice_vals)

        invoice_line_vals = self.prepare_invoice_lines(invoice_id)
        self.env['account.move.line'].create(invoice_line_vals)

    def prepare_invoice(self):
        values = {
            'move_type': 'out_invoice',
            'invoice_date': self.prescription_date,
            'partner_id': self.patient_id.partner_id.id,
            'partner_shipping_id': self.patient_id.partner_id.id,
            'company_id': self.env.company.id,
            'user_id': self.env.user.id,
                # 'invoice_line_ids': [],
        }
        return values

    def prepare_invoice_lines(self,invoice_id):
        lines = self.env['prescription.line'].search([('prescription_line_id', '=', self.id)])
        prescription_line_val = []
        for line in lines:
            line_vals = {
                'product_id': line.product_id.id,
                'quantity': line.quantity,
                'price_unit': line.price_unit,
                'price_subtotal':line.total_amount,
                'move_id' : invoice_id.id
            }
            prescription_line_val.append(line_vals)
        return prescription_line_val


    def action_create_prescription_delivery(self):
        self.state = 'ready'
        delivery_vals = self.prepare_delivery_vals()
        delivery_id = self.env['stock.picking'].create(delivery_vals)

        delivery_line_vals = self.prepare_delivery_line_vals(delivery_id)
        self.env['stock.move'].create(delivery_line_vals)

        if not delivery_line_vals:
            delivery_id.unlink()
            raise UserError('Please add product to deliver!')

        self.delivery_ids.action_confirm()
        # delivery_id.button_validate()


    def prepare_delivery_vals(self):
        picking_type_id = self.env['stock.picking.type'].search([('code','=','outgoing')], limit=1)
        values = {
            'partner_id' : self.patient_id.partner_id.id,
            'origin': self.prescription_code,
            'lead_reference': self.lead_reference,
            'location_id': picking_type_id.default_location_src_id.id,
            'location_dest_id':picking_type_id.default_location_dest_id.id,
            'picking_type_id':picking_type_id.id,
            'prescription_id':self.id,
        }
        return values

    def prepare_delivery_line_vals(self, delivery_id):
        move_val = []
        for line in self.prescription_lines:
            total_qty = sum(line.move_ids.mapped('product_uom_qty'))
            remainning_qty = line.quantity - total_qty

            if remainning_qty > 0:
                vals = {
                    'name': line.product_id.display_name,
                    'product_id': line.product_id.id,
                    'product_uom_qty': remainning_qty,
                    'location_id': delivery_id.location_id.id,
                    'location_dest_id': delivery_id.location_dest_id.id,
                    'picking_id': delivery_id.id,
                    'picking_type_id': delivery_id.picking_type_id.id,
                    'delivery_line_id': line.id,
                }
                move_val.append(vals)
        return move_val


    def action_view_prescription_delivery(self):
        form_view_id = self.env.ref('stock.view_picking_form').id
        list_view_id = self.env.ref('stock.vpicktree').id

        res = {
            'name': 'Delivery',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'stock.picking',
            'views': [(list_view_id, 'list'), (form_view_id, 'form')],
            'target': 'current',
            'domain': [('prescription_id','=',self.id)],
        }

        return res

    @api.depends("delivery_ids.prescription_id")
    def _compute_count_delivery(self):
        for record in self:
            self.delivery_count = self.env['stock.picking'].search_count([('prescription_id','=',record.id)])
