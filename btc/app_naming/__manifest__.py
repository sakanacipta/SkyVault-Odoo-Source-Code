# -*- coding: utf-8 -*-
{
    'name': "app_naming",

    'summary': "All Renaming Function",

    'description': """
    Renaming function will put under this module.
    """,

    'author': "CSH Solution Sdn Bhd (Cipta-x)",
    'website': "none",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['purchase','mail'],

    # always loaded
    'data': [
        'views/main_menu_page.xml',
        'views/Check_in_Create_PO.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

