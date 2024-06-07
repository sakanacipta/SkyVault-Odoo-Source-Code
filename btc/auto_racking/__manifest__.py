# -*- coding: utf-8 -*-
{
    "name": "auto_racking",
    "summary": """
        Odoo Auto Racking""",
    "description": """
        Long description of module's purpose
    """,
    "author": "My Company",
    "website": "http://www.yourcompany.com",
    "license": "LGPL-3",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    "category": "Uncategorized",
    "version": "17.0.0.1",
    # any module necessary for this one to work correctly
    "depends": ["base", "stock"],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "views/views.xml",
        "views/templates.xml",
        "report/auto_racking_report.xml",
        "report/auto_racking_template.xml",
        "report/skyvault_label.xml",
        "report/skyvault_label_template.xml",
        "report/skyvault_label_template_bulk.xml",
    ],
    # only loaded in demonstration mode
    "demo": [
        "demo/demo.xml",
    ],
}
