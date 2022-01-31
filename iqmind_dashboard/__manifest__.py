# -*- coding: utf-8 -*-
{
    'name': "IQMINDS - Odoo Mangement Dashboard",

    'summary': """
        This dashboard use for management""",

    'description': """
       Management can see all transactional data from one screen. Management can search 
       Sales, invoice and customer record from one screen
    """,

    'author': "IQMinds Technology",
    'website': "http://www.iqminds.com",
    'category': 'backend',
    'version': '0.1',
    'license': 'OPL-1',
    'price':50.0,
    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'account', 'purchase','stock','hr','hr_expense'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/iqminds_dashboard_view.xml',
        'views/assets.xml',
        #'views/menu.xml',
    ],
    'images': ['static/description/dashboard.png'],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
