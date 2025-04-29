from odoo import fields, models, api


class MailActivitySchedule(models.TransientModel):
    _inherit = 'mail.activity.schedule'

    meaningful_connection = fields.Boolean(string="Meaningful Connection")
