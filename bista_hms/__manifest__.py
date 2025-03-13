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

    'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence.xml',
        'data/appointment_ir_sequence.xml',
        'views/res_patient_view.xml',
        'views/hms_appointment_view.xml',
        'views/appointment_list_view.xml'
    ],
}
