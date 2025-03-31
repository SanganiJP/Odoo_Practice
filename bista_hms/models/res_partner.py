from odoo import fields, models, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    extra_discount = fields.Integer(string="Extra Discount")

    def write(self, vals):
        for record in self:
            if self.env.context.get('prevent_recursive_calls'):
                return super().write(vals)
            else:
                    patients = self.env['res.patient'].search([('partner_id','=',self.id)])
                    if patients.partner_id:
                        patient_data = {}
                        if 'name' in vals.keys():
                            patient_data['name'] = vals.get('name')
                        if 'phone' in vals.keys():
                            patient_data['phone'] = vals.get('phone')
                        if 'email' in vals.keys():
                            patient_data['email'] = vals.get('email')
                        if 'mobile' in vals.keys():
                            patient_data['mobile'] = vals.get('mobile')
                        patients.with_context(prevent_recursive_calls=True).write(patient_data)
            res = super().write(vals)
            return res
