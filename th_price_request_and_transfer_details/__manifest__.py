# -*- coding: utf-8 -*-
{
    'name': 'Détails sur les demandes de prix et tranfert de stock',
    'version': '1.2.0',
    'price': 15.99,
    'currency': 'EUR',
    'license': 'AGPL-3',
    'summary': """
       Détails sur les demandes de prix et tranfert de stock
    """,
    'category': 'Sale',
    'author': 'Thomas ATCHA',
    'maintainer': 'Thomas ATCHA',
    'company': 'Thomas ATCHA',
    'website': 'https://digitaltg.net',
    'depends': ['base', 'purchase', 'stock'],
    'data': [
        'views/price_request_view.xml',
        'views/tranfest_view.xml',
    ],

    'installable': True,
    'application': False,
    'auto_install': False,
}
