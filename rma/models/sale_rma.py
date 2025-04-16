from odoo import fields,models,api

class SaleRma(models.Model):
    _name = "sale.rma"
    _description = "order return process"
    _rec_name = 'team_id'

    team_id = fields.Char(copy=False, readonly=True, index=True, default="New", string="Team code")
    sale_team_id = fields.Many2one("team.rma",string="Team Name")
    date = fields.Date(string="Date")
    sale_order_id = fields.Many2one("sale.order", string="Sale order")
    rma_line_ids = fields.One2many("sale.rma.line","rma_id",string="RMA lines")
    delivery_ids = fields.One2many("stock.picking", "picking_id", string="Deliveries")
    delivery_count = fields.Integer(default=0, compute='_compute_delivery_count')

    @api.model_create_multi
    def create(self, vals):
        for rec in vals:
            if rec['sale_team_id']:
                team = self.env['team.rma'].browse(rec['sale_team_id'])
                prefix = team.team_prefix
                seq_name = f'Sale RMA {team.team_name}'
                seq_code = f'sale.rma.{team.id}'

                if not self.env['ir.sequence'].search([('code', '=', seq_code)], limit=1):
                    self.env['ir.sequence'].create({
                        'name': seq_name,
                        'code': seq_code,
                        'prefix': prefix,
                        'padding': 4,
                    })
                rec['team_id'] = self.env['ir.sequence'].next_by_code(seq_code)
            return super(SaleRma, self).create(vals)

    @api.onchange('sale_order_id')
    def get_rma_line(self):
        if self.sale_order_id:
            rma_lines = []
            rma_lines = [(5, 0, 0)]
            for line in self.sale_order_id.order_line:
                rma_lines.append((0, 0, {
                    'product_id': line.product_id.id,
                    'sale_order_qty': line.product_uom_qty,
                    'unit_price': line.price_unit,
                }))
            self.rma_line_ids = rma_lines

    def action_sale_rma_return_wizard(self):
        view_id = self.env.ref('rma.rma_wizard_form').id
        return {
            'name': 'Rma line qty update',
            'view_mode': 'form',
            'res_model': 'rma.wizard',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    def action_view_return_receipt(self):
        form_view_id = self.env.ref('stock.view_picking_form').id
        list_view_id = self.env.ref('stock.vpicktree').id

        res = {
            'name': 'Receipts',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'stock.picking',
            'views': [(list_view_id, 'list'), (form_view_id, 'form')],
            'target': 'current',
            'domain': [('picking_id', '=', self.id)],
        }
        return res

    @api.depends('delivery_ids.picking_id')
    def _compute_delivery_count(self):
        for rec in self:
            self.delivery_count = self.env['stock.picking'].search_count([('picking_id','=',rec.id)])


