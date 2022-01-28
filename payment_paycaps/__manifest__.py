# -*- coding: utf-8 -*-
{
    'name': "Odoo - Paycaps Payment Gateway",


    'summary': """
        Best Payment Gateway in UAE
        

        """,

    'description': """
        PayCaps is a customized payment gateway solution in UAE and throughout the Middle East providing safer, faster and user-friendly
        payment gateway for Small & Medium-Sized businesses.
        PayCaps feature-rich payments gateway solution has been built completely in house which allows us to offer a customized solution tO
        our clients to help them accept payments online through a wide range of payment channels. We also provide a highly customizable white-label
        payment gateway solutions to the businesses around the globe where brand and businesses can choose the design, payment methods and overall
        theme according to there brand.
    """,


    'author': "IQMinds Technology",
    'website': "https://www.iqminds.com/",
    'maintainer': 'IQminds Technology Pvt. Ltd.',

    'category': 'Payment Gateway',
    'version': '1.1',
    'license': 'OPL-1',
    'depends': ['base','payment','website_sale'],

    'data': [
        # 'security/ir.model.access.csv',
        'views/payment_paycaps_template.xml',
        'data/data.xml',
        'views/views.xml',
        'views/templates.xml',
        

    ],
    'images': ['static/description/img/module.png']

}
