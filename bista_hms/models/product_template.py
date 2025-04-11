from odoo import fields,models,api

class ProductTemplate(models.Model):
    _inherit = "product.template"

    def action_update_on_hand_quantity(self):
        view_id = self.env.ref('bista_hms.on_hand_qty_update_wizard_form').id

        return {
            'name': 'Update on hand quantity',
            'view_mode': 'form',
            'res_model': 'qty.update.wizard',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }