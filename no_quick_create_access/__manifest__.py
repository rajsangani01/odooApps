# -*- coding: utf-8 -*-
# License LGPL-3 (https://www.gnu.org/licenses/lgpl-3.0.en.html)

{
    "name": "Quick Create Access",
    "version": "19.0.1.0.0",
    "category": "Hidden/Tools",
    "sequence": 150,
    "summary": "Prevent users from creating or editing records directly from dropdowns",
    "author": "Dynamic TechnoLabs",
    "license": "LGPL-3",
    "price": 10.00,
    "currency": "USD",
    "depends": ["base", "web"],
    "data": [
        "views/res_users_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "no_quick_create_access/static/src/js/relational_utils_patch.js",
        ],
    },
    "demo": [],
    "installable": True,
    "application": False,
    "auto_install": False,
    "description": """
            Restrict Create & Edit in Relational Fields
            ===========================================
            
            Tired of users creating duplicate customers, products, or contacts directly from dropdowns?
            
            This module gives you **full control** over who can use "Create" and "Create and Edit..." in Many2one and Many2many fields.
            
            Features
            --------
            - Global restriction per user: completely hide "Create" options in all relational fields
            - Model-specific restriction: block only selected models (e.g. res.partner, product.product)
            - Admins are always exempt
            - Clean, non-intrusive JavaScript patch (works on all forms, kanban, etc.)
            - One-click "Clear Restrictions" button for admins
            - Fully compatible with Odoo 19 (Community & Enterprise)
            
            Perfect For
            -----------
            - Companies with strict data quality rules
            - Franchises or multi-company setups
            - Businesses that want only admins to create master data
            
            100% Open Source - LGPL-3
    """,
}
