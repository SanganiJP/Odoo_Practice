from odoo import models, fields, api
from datetime import datetime

from odoo.exceptions import UserError


class Appointment(models.Model):
    _name = "hms.appointment"
    _description = "Appointment"

    name = fields.Char(string="Appointment ID", copy=False, readonly=True, index=True, default="New")
    patient_id = fields.Many2one("res.patient", string="Name", required=True)
    appointment_date = fields.Date(string="Date", required=True, default=datetime.today())
    appointment_reason = fields.Text(string="Reason")
    state = fields.Selection([('draft', 'Draft'),
                              ('confirm', 'Confirm'),
                              ('waiting', 'Waiting'),
                              ('in_consultation', 'In Consultation'),
                              ('done', 'Done'),
                              ('cancel', 'Cancel')],
                             string="Status", default='draft')
    @api.model_create_multi
    def create(self, val_list):
        res = super(Appointment, self).create(val_list)
        for record in res:
            record.name = self.env["ir.sequence"].next_by_code('hms.appointment')
        return res

    # @api.onchange('appointment_date')
    # def validate_appointment_date(self):
    #     if self.appointment_date.day < datetime.today().day:
    #         raise UserError("Appointment date should be current date or further date!")

    @api.constrains('appointment_date')
    def validate_appointment_date(self):
        if self.appointment_date.day < datetime.today().day:
            raise UserError("Appointment date should be current date or further date!")






