from odoo import models, fields, api

class ResHospital(models.Model):
    _name = "hospital.hospital"
    _description = "hospital model"

    name = fields.Char(string="Name",required=True)
    hospital_ids = fields.One2many("res.doctor","hospital_id",string="Hospital Data")