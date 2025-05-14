# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.



{
    'name': 'Loan System',

    'summary': 'This model will help in management',

    'description':
        """
        This is our model. 
        """,

    'version': '1.0',

    'author': "Bista Solution Pvt. Ltd.",

    'depends': ['base', 'account'],

    'data': [
        'security/ir.model.access.csv',
        'data/ir_cron.xml',
        'data/mail_tmplate_data.xml',
        'views/loan_system_view.xml',
    ],

    # 'installable': True,
    # 'application': True,
    # 'auto_install': False,
}
