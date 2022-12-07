# -*- coding: utf-8 -*-
{
    'name': "product_pricelist_prices",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.ictstudio.eu",
    'category': 'Sales Management',
    'version': '0.1',
    'depends': ['base','product'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_pricelist.xml',
        'views/product_product.xml',
        'views/product_template.xml',
        'views/templates.xml',
    ],

    'installable': True,
}
