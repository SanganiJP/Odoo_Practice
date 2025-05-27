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

    'depends': ['base', 'mail'],

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/room_category_records.xml',
        'data/hotel_room_records.xml',
        'data/ir_sequence.xml',
        'data/mail_template_data.xml',
        'data/ir_cron.xml',
        'views/hotel_booking_view.xml',
        'views/hotel_guest_view.xml',
        'views/hotel_room_view.xml',
        'views/hotel_room_category_view.xml',
    ],
    'license': 'LGPL-3',
}

