# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Payment Customize',

    'summary': 'This model will help in management',

    'description':
        """
        This is our management system model. 
        """,

    'version': '1.0',

    'author': "Bista Solution Pvt. Ltd.",

    'depends': ['base', 'product', 'sale', 'stock', 'mrp', 'purchase', 'mail'],

    # 'depends': ['base','product','sale','stock'],

    'data': [
        'security/ir.model.access.csv',
        'views/account_payment_view.xml',
    ],
    'license': 'LGPL-3',
}

