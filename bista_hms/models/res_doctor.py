from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ResDoctor(models.Model):
    _name = "res.doctor"
    _description = "Doctor model"

    name = fields.Many2one("res.partner", string="Name", required=True)
    doctor_specialization = fields.Many2one("hospital.specialization", string="Specialization")
    license_no = fields.Char(string="License no", required=True)
    experience_years = fields.Integer(string="Experience years")
    hospital_id = fields.Many2one("hospital.hospital",string="Hospital Name")
    is_emergency_available = fields.Boolean()

    @api.constrains('license_no')
    def _check_license_no(self):
        for rec in self:
            domain = [('license_no', '=', rec.license_no)]
            count = self.sudo().search_count(domain)
            if count > 1:
                raise ValidationError("The license No should be unique")