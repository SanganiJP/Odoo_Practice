from datetime import date, timedelta

from odoo import models, fields, api


class HmsPrescription(models.Model):
    _name = "hms.prescription"
    _description = "hms prescription"
    _rec_name = "patient_id"

    prescription_code = fields.Char(string="Prescription ID", default="New")
    patient_id = fields.Many2one("res.patient", string="Patient Name", required=True)
    prescription_date = fields.Date(string="Prescription Date", default=date.today())
    prescription_lines = fields.One2many("prescription.line", "prescription_line_id", string="Prescription")
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
