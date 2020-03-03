# -*- coding: utf-8 -*-
# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

{
    'name': 'Account Fiscal Year',
    'version': '1.0',
    'summary': 'Manage fiscal years and its periods',
    'category': 'Accounting',
    'sequence': 1,
    'author': 'Synconics Technologies Pvt. Ltd.',
    'website': 'www.synconics.com',
    'description': """
        1 Manage fiscal years and its periods.
        2 Generating opening and closing entries for fiscal year.
        3 Option to cancel opening entry.
    """,
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'data/data_account_type.xml',
        'wizard/account_move_reversal_view.xml',
        'wizard/account_period_close_view.xml',
        'wizard/account_fiscalyear_close_view.xml',
        'wizard/account_open_closed_fiscalyear_view.xml',
        'wizard/account_fiscalyear_close_state_view.xml',
        'views/account_fiscal_year_view.xml',
        'views/account_payment_view.xml',
        'views/account_view.xml',
        'views/account_menuitem.xml',
    ],
    'images': [
        'static/description/main_screen.jpg',
    ],
    'price': 130,
    'currency': 'EUR',
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'OPL-1',
}
