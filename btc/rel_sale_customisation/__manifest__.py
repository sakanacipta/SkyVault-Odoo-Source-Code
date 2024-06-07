# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Sale Customisation',
    'version' : '17.0.0.1',
    'summary': 'Inbound and outbound changes',
    'sequence': 10,
    'description': """Sale and Purchase Chamges """,
    'category': '',
    'website': '',
    'depends': ['base','contacts','sale_management','purchase','product','stock','stock_barcode','delivery_order_app'],
    'data': [
        'data/cron.xml',
        'security/ir.model.access.csv',
             'views/res_company.xml',
        'views/sale_order.xml',
             'views/product_pricelist.xml',
             'views/stock_move.xml',
             'views/stock_locations.xml',
    'views/stock_count_lines.xml'],
    'demo': [
    ],
    # 'installable': False,
    'application': True,
    # 'assets': { },
    'license': 'LGPL-3',
}
