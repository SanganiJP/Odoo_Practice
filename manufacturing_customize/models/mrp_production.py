from odoo import api, fields, models

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    lot_ids = fields.Many2many("stock.lot",string="Serial Numbers")

    def action_assign_serial_wizard(self):
        view_id = self.env.ref('manufacturing_customize.assign_serial_wizard_form').id
        return {
            'name': 'Assign serial',
            'view_mode': 'form',
            'res_model': 'assign.serial.wizard',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    # def button_mark_done(self):
    #     res = super().button_mark_done()
    #     # pass
    #     # lot_producing_id = self.lot_producing_id.id
    #     self.lot_ids = (3,self.lot_producing_id.id)
    #     return res