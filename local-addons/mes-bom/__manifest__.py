# -*- coding: utf-8 -*-
{
    'name': "mes-bom",

    'summary': """
        Bill of materials""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mrp', 'product'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/mes_bom.xml',
        'views/mes_views_menu.xml',
        'views/mes_product.xml',
        'views/mes_manufacturing_order.xml',
        # 'views/actions.xml',
        'data/mes_bom_sample_data.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'mes-bom/static/src/components/*/*.js',
            'mes-bom/static/src/components/*/*.xml',
            'mes-bom/static/src/components/*/*.scss',
        ],
    },

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
