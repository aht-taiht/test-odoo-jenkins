# -*- coding: utf-8 -*-
{
    'name': "Onnet stock picking",
    'summary': """
        """,
    'description': """
    """,
    'author': "Onnet",
    'version': '1.0',
    'license': 'LGPL-3',

    'depends': [
        'stock',
        'sale',
        'sale_stock'
    ],
    'installable': True,
    'application': True,
    'sequence': 1,
    'data': [
        'views/stock_picking_view.xml',
    ]
}
