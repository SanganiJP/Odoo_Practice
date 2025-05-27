# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Hotel Management System',

    'summary': 'This model will help in management',

    'description':
        """
        This is our model. 
        """,

    'version': '1.0',

    'author': "Bista Solution Pvt. Ltd.",

    'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',
        'data/room_category_records.xml',
        'data/hotel_room_records.xml',
        'data/ir_sequence.xml',
        'views/hotel_booking_view.xml',
        'views/hotel_room_view.xml',
        'views/hotel_room_category_view.xml',
    ],
    'license': 'LGPL-3',
    # 'installable': True,
    # 'application': True,
    # 'auto_install': False,
}

# --limit-time-cpu=6000 --limit-time-real=10000
