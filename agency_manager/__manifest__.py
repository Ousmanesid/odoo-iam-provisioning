{
    'name': "Agency Manager",
    'version': '1.0',
    'author': "Taiishiro - Ousmanesid",
    'category': 'Business',
    'summary': "Gestion des agences ubercircuit",
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/agency_view.xml',
    ],
    'demo': [
        'data/demo_data.xml',
    ],
    'installable': True,
    'application': True,
} 