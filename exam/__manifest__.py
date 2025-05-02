# {
#     'name': 'Example',
#     'version': '1.0',
#     'summary': 'Summery',
#     'description': 'Description',
#     'author': 'Author',
#     'depends': ['base', 'sale', 'purchase','product','crm','stock'],
#     'data': [
#         'security/ir.model.access.csv',
#         'views/product_detail_view.xml',
#     ],
#     'installable': True,
#     'auto_install': False
# }
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Safari',

    'summary': 'This model will help in management',

    'description':
        """
        This is our sale rma model. 
        """,

    'version': '1.0',

    'author': "Jayesh Sangani",

    'depends': ['base', 'sale', 'purchase','product','crm','stock'],

    'data': [
        'security/ir.model.access.csv',
        'views/product_detail_view.xml',
    ],
}
