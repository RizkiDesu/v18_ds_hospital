{
    'name': "Hospital BASE",
    'summary': """
        Modul Hospital BASE""",

    'description': """
        Modul Hospital BASE
    """,

    'author'    : "Lolidesu",
    'website'   : "http://www.lolidesu.my.id",
    'category'  : 'Services',
    'version'   : '18.0',
    'license'   : 'OPL-1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
    ],

    # always loaded
    'data': [
        'security/res_groups.xml',
        
        'security/ir.model.access.csv',

        
        'views/menu.xml',
        'views/patient.xml',
        # 'views/doctor.xml',
        # 'views/categ.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}


