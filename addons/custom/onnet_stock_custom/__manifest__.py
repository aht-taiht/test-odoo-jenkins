# -*- coding: utf-8 -*-
{
    'name': "Onnet stock custum",
    'summary': """
        """,
    'description': """
    """,
    'author': "Onnet",
    'version': '1.0',
    'license': 'LGPL-3',

    'depends': [
        'stock',
    ],
    'installable': True,
    'application': True,
    'sequence': 1,
    'data': [
        'views/stock_quant_parent_views.xml',
        'security/ir.model.access.csv'
    ]
}
