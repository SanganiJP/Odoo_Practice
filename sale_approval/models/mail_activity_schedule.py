from odoo import fields,models,api

class MailActivitySchedule(models.TransientModel):
    _inherit = "mail.activity.schedule"

    date = fields.Date(string="Date")