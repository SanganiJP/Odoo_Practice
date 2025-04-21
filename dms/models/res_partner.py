from odoo import fields, models, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    tag_ids = fields.Many2many("documents.tag.master",string="Master Tags")