# -*- coding: utf-8 -*-
##############################################################################
#
#    TL Technology
#    Copyright (C) 2019 ­TODAY TL Technology (<https://www.posodoo.com>).
#    Odoo Proprietary License v1.0 along with this program.
#
##############################################################################
{
    'name': "POS Base",
    'version': '1.0',
    'category': 'Point of Sale',
    'author': 'TL Technology',
    'sequence': 0,
    'summary': 'POS Base',
    'description': 'This is base pos addons of POS TL Technology',
    'depends': ['point_of_sale'],
    'data': [
        'import.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml'
    ],
    'price': '10',
    "currency": 'EUR',
    'website': 'http://posodoo.com',
    'application': True,
    'images': ['static/description/icon.png'],
    'support': 'thanhchatvn@gmail.com',
    "license": "OPL-1",
}
