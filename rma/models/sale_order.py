from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if not args:
            args = []
        partner_id = self.env.context.get('partner_id')
        if partner_id:
            args = [('partner_id.id', '=', partner_id)]
        else:
            return super().name_search(name, args, operator=operator, limit=limit)
        sale_orders =  self.search_fetch(args, ['name'], limit=limit)
        return [(name.id, name.display_name) for name in sale_orders.sudo()]

    @api.model
    @api.readonly
    def web_search_read(self, domain, specification, offset=0, limit=None, order=None, count_limit=None):
        partner_id = self.env.context.get('partner_id')
        if partner_id:
            domain += ([('partner_id.id', '=', partner_id)])
        return super().web_search_read(domain, specification, offset=offset, limit=limit, order=order, count_limit=count_limit)


