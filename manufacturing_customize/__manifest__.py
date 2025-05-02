# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Bista Production',

    'summary': 'This model will help in management',

    'description':
        """
        This is our management system model. 
        """,

    'version': '1.0',

    'author': "Bista Solution Pvt. Ltd.",

    'depends': ['base', 'product', 'sale', 'stock', 'contacts', 'purchase', 'mail'],

    # 'depends': ['base','product','sale','stock'],

    'data': [
        'security/ir.model.access.csv',
        'views/product_product_view.xml',
        'views/mrp_production_view.xml',
        'views/sale_order_view.xml',
        'wizard/assign_serial_wizard.xml',
    ],
}

