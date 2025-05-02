from . import sale_rma_add_product_wizard

# selection field============
# state = fields.Selection([('draft', 'Draft'),
#                               ('confirm', 'Confirmed'),
#                               ('ready', 'Ready'),
#                               ('done','Done'),
#                               ('cancel', 'Cancelled')],
#                              string="Status", default='draft')

# wizard=======================
# <button name="action_sale_rma_add_product_wizard" class="btn-primary" type="object" string="Add Product"/>
# def action_sale_rma_add_product_wizard(self):
#     view_id = self.env.ref('rma.sale_rma_add_product_wizard_form').id
#     return {
#         'name': 'Add Product',
#         'view_mode': 'form',
#         'res_model': 'sale.rma.add.product.wizard',
#         'view_id': view_id,
#         'type': 'ir.actions.act_window',
#         'target': 'new',
#     }

# options="{'no_create': True, 'no_create_edit':True}

# sequence==================
# <?xml version="1.0" encoding="utf-8"?>
#
# <odoo noupdate="1">
#     <record id="sequence_res_patient" model="ir.sequence">
#         <field name="name">Res patient</field>
#         <field name="code">res.patient</field>
#         <field name="prefix">P-</field>
#         <field name="padding">4</field>
#     </record>
# </odoo>
#
# @api.model_create_multi
# def create(self, val_list):
#     res = super(HmsPrescription, self).create(val_list)
#     for record in res:
#         record.prescription_code = self.env["ir.sequence"].next_by_code('hms.prescription')
#     return res

#system parameter
# <odoo>
#     <record id="unique_id_for_parameter" model="ir.config_parameter">
#         <field name="key">your.key.name</field>
#         <field name="value">your_value_here</field>
#     </record>
# </odoo>
#
# 'data': [
#     'data/ir_config_parameter_data.xml',
# ],
#
# self.env['ir.config_parameter'].sudo().get_param('your.key.name')
#
# self.env['ir.config_parameter'].sudo().set_param('your.key.name', 'your_value')



