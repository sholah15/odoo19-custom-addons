{
    'name': "Safe Fields Tester",
    'version': '19.0.0.1',
    'summary': "Test module for safe field access",
    'description': """
    Test module for safe field access
    """,
    'author': "Maizar",
    'website': "https://maizarrahman.blogpost.com",
    'category': 'Tools',
    'license': 'LGPL-3',
    'depends': ['base', 'safe_fields'],
    'data': [
        'security/ir.model.access.csv',
        'views/safe_fields_tester_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
