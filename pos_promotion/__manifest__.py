    # -*- coding: utf-8 -*-
{
    'name': "POS Promotions",
    'version': '3.3',
    'live_test_url': 'http://posodoo.com/web/signup',
    'category': 'Point of Sale',
    'author': 'TL Technology',
    'sequence': 0,
    'summary': 'POS Promotions',
    'description': 'POS Promotions',
    'depends': ['pos_base'],
    'data': [
        'security/ir.model.access.csv',
        'data/product_data.xml',
        'import/template.xml',
        'views/pos_promotion.xml',
        'views/pos_config.xml',
        'views/pos_order.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml'
    ],
    'price': '100',
    'website': 'http://posodoo.com',
    'application': True,
    'images': ['static/description/icon.png'],
    'support': 'thanhchatvn@gmail.com',
    "currency": 'EUR',
    "license": "OPL-1"
}
