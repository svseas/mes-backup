# -*- coding: utf-8 -*-
{
    "name": "mes-bom-ui",
    "summary": """
        Bill of materials with UI""",
    "description": """
        Long description of module's purpose
    """,
    "author": "Long Nguyen <intihad.vuong@gmail.com>",
    "website": "https://www.merctechs.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Uncategorized",
    "version": "0.1",
    # any module necessary for this one to work correctly
    "depends": ["base", "mrp", "product", "mes-bom", "web"],
    # always loaded
    "data": [
        # 'security/ir.model.access.csv',
        "views/views.xml",
        "views/templates.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "mes-bom-ui/static/src/components/*/*.js",
            "mes-bom-ui/static/src/components/*/*.xml",
            "mes-bom-ui/static/src/components/*/*.scss",
        ],
    },
    # only loaded in demonstration mode
    "demo": [],
}
