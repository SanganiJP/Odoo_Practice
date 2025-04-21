# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Bista DMS',

    'summary': 'This model will help in management',

    'description':
        """
        This is our management system model. 
        """,

    'version': '1.0',

    'author': "Bista Solution Pvt. Ltd.",

    'depends': ['base','product','sale','stock'],

    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_view.xml',
        'views/product_template_view.xml',
        'views/sale_order_view.xml',
        'views/documents_custom_view.xml',
    ],
}
