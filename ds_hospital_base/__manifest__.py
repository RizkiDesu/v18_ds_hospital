{
    'name': "Hospital Base",
    'summary': """
        Modul Hospital Base""",

    'description': """
        Modul Hospital Base
    """,

    'author'    : "Lolidesu",
    'website'   : "http://www.lolidesu.my.id",
    'category'  : 'Services',
    'version'   : '18.0',
    'license'   : 'OPL-1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'contacts',
        'hr',
        'stock',
        'account',
    ],

    # always loaded
    'data': [
        'security/res_groups.xml',
        'security/ir.model.access.csv',

        'data/ir_sequence.xml',

        'views/menu.xml',
        'views/patient.xml',

        'views/inherit_res_parner.xml',
        'views/inherit_hr_employee.xml',
        'views/inherit_res_config_settings.xml',

        'views/hospital_service.xml',
        'views/inherit_res_company.xml',
        'views/inherit_product_template.xml',
        'views/inherit_account_move.xml',

        # Areas
        'views/province.xml',
        'views/city.xml',
        'views/district.xml',
        'views/sub_district.xml',
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/ds_patiens.xml',
    # ],
}


