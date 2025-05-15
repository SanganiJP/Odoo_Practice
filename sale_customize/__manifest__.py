# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Sale Customize',

    'summary': 'This model will help in delivery management',

    'description':
        """
        This is our Hospital management system model. 
        """,

    'version': '1.0',

    'author': "Jayesh Sangani",

    'depends': ['base','sale','stock','sale_stock'],

    'data': [
        'views/sale_order_view.xml',
    ],
    'license': 'LGPL-3',
}

