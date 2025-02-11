{
    'name': 'Policy',
    'summary': 'This module is used for handle HR Policies',
    'description': """This module allows the company to upload and manage policy documents,"
                   making them accessible to all employees.""",
    'category': 'Human Resources',
    'version': '17.0.1.0.0',
    'depends': ['mail', 'hr'],
    'author': 'Adil PK',
    'company': 'Tijus Academy',
    'website': "https://tijusacademy.com/",
    'data': [
        'data/mail_activity_data.xml',
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
        'views/hr_policy_view.xml',
        'views/policy_tag_view.xml',
        'views/hr_policy_menu.xml',
    ],
    'license': 'LGPL-3',
    'application': False,

}
