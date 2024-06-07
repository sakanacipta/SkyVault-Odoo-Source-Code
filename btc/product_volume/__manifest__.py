{
    'name': 'Product Volume Calculation',
    'version': '17.0.1.1.0',
    'category': "Inventory",
    'summary': """This module will helps you to give dimensions of the product.""",
    'description': "Module helps you to manage the length, breadth and height "
                   "of the product and calculates its volume accordingly.",
    'depends': ['stock'],
    'data': [
        'views/product_template_views.xml'
    ],
    'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
