# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'SOA',

    'summary': 'This model will help management',

    'description':
        """
        This is our Hospital management system model. 
        """,

    'version': '1.0',

    'author': "Bista Solution Pvt. Ltd.",

    'depends': ['base','product','sale','stock'],

    'data': [
        'data/ir_cron.xml',
        'data/mail_template_data.xml',
        'views/res_config_settings_views.xml',
        'views/sale_order_view.xml',
        'views/purchase_order_view.xml',
        'views/chatter_activity_view.xml',
    ],
    'license': 'LGPL-3',
}

