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
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/ir_cron.xml',
        'data/product_record.xml',
        'data/mail_template_data.xml',
        'views/loan_system_view.xml',
        'views/loan_approval_team.xml',
        'views/approval_levels_view.xml',
    ],
    'license': 'LGPL-3',
    # 'installable': True,
    # 'application': True,
    # 'auto_install': False,
}
