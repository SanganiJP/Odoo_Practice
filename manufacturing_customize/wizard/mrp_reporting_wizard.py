from odoo import models, fields
from io import BytesIO
import xlsxwriter
import base64


class MrpReportingWizard(models.TransientModel):
    _name = "mrp.reporting.wizard"
    _description = "description"

    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")

    def download_report(self):
        # Step 1: Create Excel in memory
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        bold = workbook.add_format({'bold': True})

        headers = [
            'Manufacturing Order',
            'Product',
            'Quantity',
            'Scheduled Start Date',
            'Production State',
            'Component Name',
            'Component Quantity'
        ]

        for col, header in enumerate(headers):
            worksheet.write(0, col, header, bold)

        # worksheet.write('A1', 'MO', bold)
        # worksheet.write('B1', 'Product', bold)
        # worksheet.write('C1', 'Quantity', bold)
        # worksheet.write('D1', 'Scheduled Date', bold)
        # worksheet.write('E1', 'State', bold)
        # worksheet.write('F1', 'Component Product', bold)
        # worksheet.write('G1', 'Component Quantity', bold)

        row = 1

        records = self.env["mrp.production"].search([
            ('date_start', '>', self.start_date),
            ('date_start', '<', self.end_date)
        ])

        for rec in records:
            worksheet.write(row, 0, rec.name)
            worksheet.write(row, 1, rec.product_id.name)
            worksheet.write(row, 2, rec.product_qty)
            worksheet.write(row, 3, rec.date_start.strftime("%d-%m-%Y"))
            worksheet.write(row, 4, rec.state)
            for component in rec.move_raw_ids:
                worksheet.write(row, 5, component.product_id.name)
                worksheet.write(row, 6, component.quantity)
                row += 1

        workbook.close()
        output.seek(0)

        # Step 2: Encode and create attachment
        file_data = output.read()
        attachment = self.env['ir.attachment'].create({
            'name': 'mrp_report.xlsx',
            'type': 'binary',
            'datas': base64.b64encode(file_data),
            'res_model': self._name,
            'res_id': self.id,
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        })

        # Step 3: Return URL to download the attachment
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'new',
        }




