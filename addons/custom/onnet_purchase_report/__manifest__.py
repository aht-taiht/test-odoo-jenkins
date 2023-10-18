# -*- coding: utf-8 -*-
{
    'name': "Onnet purchase reports",
    'summary': """
        """,
    'description': """
    """,
    'author': "Onnet",
    'version': '1.0',
    'license': 'LGPL-3',

    'depends': [
        'sale',
    ],
    'installable': True,
    'application': True,
    'sequence': 1,
    'data': [
        'views/purchase_order_lines.xml'
    ]
}
