{
    'name': "Hospital Observation Services",
    'summary': """
        Modul Hospital Observation Services""",

    'description': """
        Modul Hospital Observation Services
    """,

    'author'    : "Lolidesu",
    'website'   : "http://www.lolidesu.my.id",
    'category'  : 'Services',
    'version'   : '18.0',
    'license'   : 'OPL-1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'ds_hospital_base',
    ],

    # always loaded
    'data': [
        # 'security/res_groups.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence.xml',
        'views/observation_service.xml',

    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/ds_patiens.xml',
    # ],
}


