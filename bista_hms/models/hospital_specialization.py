from odoo import models, fields, api

class HospitalSecialization(models.Model):
    _name = "hospital.specialization"
    _description = "Doctor`s specialization model"

    name = fields.Char(string="Name",required=True)
    doctors_ids = fields.One2many("res.doctor","doctor_specialization",string="doctor specialization")