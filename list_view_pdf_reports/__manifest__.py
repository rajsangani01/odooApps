# -*- coding: utf-8 -*-
{
    'name': 'List View PDF Reports | Direct PDF Download from List Rows',
    'summary': 'Download available PDF reports directly from record rows in Odoo List Views',
    'description': """
List View PDF Reports (Odoo 19.0)
=================================
Allows users to view and download available PDF reports directly from record rows in Odoo List (Tree) Views.

Key Features:
- Direct PDF report dropdown action on List View rows
- Automatic hover dropdown menu with high z-index unclipped popups
- Dynamic report discovery based on active model
- Conditional display (renders ONLY when at least one active report is available)
- Full adherence to Odoo access rights (ACLs), user groups, record rules, and multi-company security
- Minimal RPC overhead with cached model report metadata
- Administrator settings to toggle report visibility in List View
""",
    'author': 'Rajkumar Sangani',
    'support': 'rajodoobot@gmail.com',
    'website': 'mailto:rajodoobot@gmail.com',
    'category': 'Extra Tools',
    'version': '19.0.1.0.0',
    'license': 'OPL-1',
    'price': 29.00,
    'currency': 'EUR',
    'images': [
        'static/description/banner.png',
    ],
    'depends': ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/ir_actions_report_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'list_view_pdf_reports/static/src/views/list/list_renderer_patch.scss',
            'list_view_pdf_reports/static/src/views/list/list_renderer_patch.js',
            'list_view_pdf_reports/static/src/views/list/list_renderer_patch.xml',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
