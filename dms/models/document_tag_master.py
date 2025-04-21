from odoo import fields, models, api


class DocumentsTagMaster(models.Model):
    _name = "documents.tag.master"
    _description = "This is our Model"

    name = fields.Char(string="Tag")
