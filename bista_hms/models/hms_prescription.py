from datetime import date, timedelta
from email.policy import default

from odoo import models, fields, api


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
                              ('cancel', 'Cancelled')],
                             string="Status", default='draft')

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


    def action_view_prescription_delivery(self):
        form_view_id = self.env.ref('stock.view_picking_form').id

        res = {
            'name': 'Delivery',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'stock.picking',
            'target': 'current',
            'view_id': form_view_id,
            'context': dict(default_partner_id=self.patient_id.partner_id.id, default_origin=self.prescription_code, default_lead_reference=self.lead_reference)
            # 'context': dict(default_partner_id=self.partner_id.id, default_picking_type_id=picking_id.picking_type_id.id, default_origin=self.name, default_group_id=picking_id.group_id.id)
        }
        return res
