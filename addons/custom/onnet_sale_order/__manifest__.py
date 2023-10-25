# -*- coding: utf-8 -*-
{
    'name': "Onnet sales order",
    'summary': """
        """,
    'description': """
    """,
    'author': "Onnet",
    'version': '1.0',
    'license': 'LGPL-3',

    'depends': [
        'sale',
        'sale_management',
        'account'
    ],
    'installable': True,
    'application': True,
    'sequence': 1,
    'data': [
        'views/sale_order_view.xml'
    ]
}