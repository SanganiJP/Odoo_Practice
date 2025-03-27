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

    'depends': ['base','product','sale'],

    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence.xml',
        'data/appointment_ir_sequence.xml',
        'data/ir_cron.xml',
        'views/res_patient_view.xml',
        'views/hms_appointment_view.xml',
        'views/res_doctor_view.xml',
        'views/hms_prescription_view.xml',
        'views/prescription_line_view.xml',
        'views/sale_order_view.xml',
        'views/res_partner_view.xml',
        'views/sale_order_line_view.xml',
        'wizard/date_practice_wizard_view.xml',
    ],
}
