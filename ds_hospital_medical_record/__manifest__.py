{
    'name': "Hospital Medical Record",
    'summary': """
        Modul Hospital Medical Record""",

    'description': """
        Modul Hospital Medical Record
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
        'ds_hospital_observation_services',
    ],

    # always loaded
    'data': [
        'security/res_groups.xml',
        # 'security/ir.model.access.csv',
        # 'data/ir_sequence.xml',
        # 'data/data.xml',
        'views/menu.xml',
        # 'views/inherit_res_config_settings.xml',
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/ds_patiens.xml',
    # ],
}


