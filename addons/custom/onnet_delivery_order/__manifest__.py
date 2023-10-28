# -*- coding: utf-8 -*-
{
    'name': "Onnet Delivery Order",
    'summary': 'Custom module for Onnet Delivery Order',
    'description': """
    """,
    'author': "Onnet",
    'version': '1.0',
    'sequence': 25,
    'depends': [
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/delivery_type_view.xml',
        'views/delivery_type_menu.xml'
    ]
}
