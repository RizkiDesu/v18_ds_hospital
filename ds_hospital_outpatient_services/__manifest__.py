{
    'name': "Hospital Outpatient Services",
    'summary': """
        Modul Hospital Outpatient Services""",

    'description': """
        Modul Hospital Outpatient Services
    """,

    'author'    : "Lolidesu",
    'website'   : "http://www.lolidesu.my.id",
    'category'  : 'Services',
    'version'   : '18.0',
    'license'   : 'OPL-1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'stock',
        'account',
        'ds_hospital_base',
        'ds_hospital_observation_services',
    ],

    # always loaded
    'data': [
        'security/res_groups.xml',
        'security/ir.model.access.csv',

        'data/ir_sequence.xml',
        'data/data.xml',

        'views/menu.xml',
        'views/registration_outpatient.xml',
        'views/inherit_res_config_settings.xml',


        
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/ds_patiens.xml',
    # ],
}


