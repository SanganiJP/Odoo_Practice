# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'School Management',

    'summary': 'This our school management system',

    'description':
        """
        This is our first model. 
        """,

    'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',
        'views/school_management_views.xml',
    ],
}