from odoo import fields, models, api
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"
    _description = "Purchase Order"

    def button_confirm(self):
        res = super().button_confirm()
        if self.partner_id.email:
            template_id = self.env.ref('practical_jayesh.purchase_order_confirmation_mail_template')
            template_id.send_mail(self.id, force_send=True)
        else:
            UserError('No email found!')
        return res




