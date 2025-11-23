# -*- coding: utf-8 -*-

{
    'name': 'Restrict Relational Field Creation',
    'version': '1.0',
    'summary': 'User-configurable control for relational field creation/editing permissions.',
    'description': """
        Allows administrators to restrict relational field "Create" and "Create and Edit..."
        shortcuts globally or per model. Supports per-user/group configurations.
    """,
    'category': 'Security',
    'author': 'Rajkumar Sangani',
    'license': 'LGPL-3',
    'depends': ['base', 'web'],
    'data': [
        "views/res_users_views.xml",
    ],
    'assets': {
        'web.assets_backend': [
            'restrict_relational_create_pro/static/src/js/**/*',
        ],
    },
    'installable': True,
}
