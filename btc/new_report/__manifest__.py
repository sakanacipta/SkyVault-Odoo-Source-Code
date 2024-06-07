# -*- coding: utf-8 -*-
{
    "name": "New Report",
    "version": "1.0",
    "summary": "Custom Reports",
    "sequence": -100,
    "description": """Good Received Note, Delivery Order, Purchase Order etc.""",
    "author": "Chong",
    "license": "AGPL-3",
    "depends": ["stock", "purchase", "sale"],
    "data": [
        # view
        "views/sale_view.xml",
        "views/purchase_view.xml",
        "views/stock_view.xml",
        # report
        "report/report.xml",
        # official report
        "report/good_received_note.xml",
        "report/purchase_order.xml",
        "report/delivery_order.xml",
        "report/unloading.xml",
        "report/pick_list.xml",
        "report/putaway_list.xml",
    ],
    "demo": [],
    "qweb": [],
    "installable": True,
    "application": True,
    "auto_install": False,
}
