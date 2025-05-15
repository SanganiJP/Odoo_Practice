# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Bista CRM',

    'summary': 'This model will help in CRM',

    'description':
        """
        This is our CRM model. 
        """,

    'version': '1.0',

    'author': "Bista Solution Pvt. Ltd.",

    'depends': ['base', 'sale', 'crm'],

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/crm_lead_view.xml',
        'views/probability_stages_view.xml',
        'views/student_activity_view.xml',
    ],
    'license': 'LGPL-3',
}
