# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Student Management',

    'summary': 'This our student management system',

    'version': '1.0',

    'author': "Sangani Jayesh",

    'description':
        """
        This is our student management system model. 
        """,

    'depends': ['base','product'],

    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence.xml',
        'data/ir_corn.xml',
        'views/res_student_views.xml',
        'views/res_subject_views.xml',
        # 'views/previous_year_marks_views.xml',
        'views/tuition_fee_structure_views.xml',
    ],
}