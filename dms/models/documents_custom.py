from odoo import fields,models,api

class DocumentsCustom(models.Model):
    _name = "documents.custom"
    _description = "This is our Model."

    name = fields.Char(string="Document Name")
    attachment_id = fields.Many2one("ir.attachment",string="Document Name")
    tag_ids = fields.Many2many("document.tag.master",string="Tags")