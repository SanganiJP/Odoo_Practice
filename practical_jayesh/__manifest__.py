# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Jayesh',

    'summary': 'This model will help in management',

    'description':
        """
        This is our model. 
        """,

    'version': '1.0',

    'author': "Bista Solution Pvt. Ltd.",

    'depends': ['base','product','sale','stock','contacts','purchase','mail'],

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/mail_template_data.xml',
        'data/pharmacy_record.xml',
        'views/account_move_view.xml',
        'views/chatter_activity_view.xml',
        'views/res_config_settings_views.xml',
        'views/sale_order_view.xml',
        'views/delivery_slip_report.xml',
        'views/pharmacy_view.xml',
        'views/product_template_view.xml',
        # 'views/stock_picking_view.xml',
        'wizard/add_product_wizard_form.xml',
    ],

    # 'installable': True,
    # 'application': True,
    # 'auto_install': False,
}
