# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Project Management',

    'summary': 'This our project management system',

    'description':
        """
        This is our first model. 
        """,

    'version': '1.0',

    'author': "Author Name",

    'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',
        'views/project_management_views.xml',
        'views/project_lead_views.xml',
        'views/project_types_views.xml',
        'wizard/project_info_wizard_view.xml',
    ],

}