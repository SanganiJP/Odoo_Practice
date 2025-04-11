from odoo import models,fields,api

class RmaLineWizard(models.TransientModel):
    _name = "rma.wizard"
    _description = "qty update wizard"

    record_id = fields.Integer(string="Record ID")
    wizard_rma_lines_ids = fields.One2many("wizard.rma.lines","wizard_rma_line_id", string=" ")


    def default_get(self, fields_list):
        res = super(RmaLineWizard, self).default_get(fields_list)
        res['record_id'] = self.env.context.get('active_id')
        return res

    def process_return(self):
        pass
        # records = self.env['sale.rma'].browse(self.record_id)
        # print(records)
        # for rec in records.rma_line_ids:
        #     print(rec.sale_order_qty)
        #     rec.received_qty = 1
        #     rec.received_qty = self.env['wizard.rma.lines'].search([('wizard_rma_line_id','=',rec.id)])

        # return_qty = {}
        # records = self.env['sale.rma'].browse(self.record_id)
        # for rec in self.wizard_rma_lines_ids:
        #     return_qty['received_qty'] = rec.qty
        # records.write(1,records.rma_id,return_qty)


    @api.onchange('record_id')
    def onchange_sale_order(self):
        if self.record_id:
            records = self.env['sale.rma'].browse(self.record_id)
            rma_lines = []
            rma_lines = [(5, 0, 0)]
            for line in records.rma_line_ids:
                rma_lines.append((0, 0, {
                    'product_id': line.product_id.id,
                    'so_qty': line.sale_order_qty,
                }))
            self.wizard_rma_lines_ids = rma_lines
