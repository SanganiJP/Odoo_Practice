# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'RMA',

    'summary': 'This model will help in return management',

    'description':
        """
        This is our sale rma model. 
        """,

    'sequence':1,
    'version': '1.0',

    'author': "Bista Solution Pvt. Ltd.",

    'depends': ['base', 'sale'],

    'data': [
        'security/ir.model.access.csv',
        'views/sale_rma_view.xml',
        'views/team_rma_view.xml',
        'wizard/sale_rma_return_wizard.xml'
    ],
}
