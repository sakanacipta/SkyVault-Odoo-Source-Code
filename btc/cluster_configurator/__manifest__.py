# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Custom Stock Cluster',
    'version': '17.0.0.1',
    'summary': 'Manage Stock Clusters',
    'description': """Manage Stock Clusters""",
    'category': 'Inventory',
    'website': 'esspl.com',
    'license': 'LGPL-3',
    'depends': ['base', 'stock','rel_sale_customisation'],
    'data': [
        'security/ir.model.access.csv',
        'views/stock_cluster.xml',
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}

