# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Bista HMS',

    'summary': 'This model will help in hospital management',

    'description':
        """
        This is our Hospital management system model. 
        """,

    'version': '1.0',

    'author': "Bista Solution Pvt. Ltd.",

    'depends': ['base','product','sale','stock'],

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence.xml',
        'data/appointment_ir_sequence.xml',
        'data/ir_cron.xml',
        'data/mail_tmplate_data.xml',
        'views/res_patient_view.xml',
        'views/hms_appointment_view.xml',
        'views/res_doctor_view.xml',
        'views/hms_prescription_view.xml',
        'views/prescription_line_view.xml',
        'views/sale_order_view.xml',
        'views/res_partner_view.xml',
        'views/stock_picking_view.xml',
        'views/prescription_report_templete.xml',
        'views/report.xml',
        'views/product_template_view.xml',
        'views/sale_order_report_template.xml',
        'wizard/date_practice_wizard_view.xml',
        'wizard/on_hand_qty_update_wizard_view.xml',
    ],
}
