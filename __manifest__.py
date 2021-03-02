# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Hospital Management',
    'version' : '0.1',
    'summary': 'Hospital Management Software',
    'sequence': -10,
    'description': """Hospital Management Software""",
    'category': 'Productivity',
    'website': 'https://www.abcxyz.com/',
    'license': 'LGPL-3',
    'depends': ['sale', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/patient.xml',
        'views/appointment.xml',
        'views/doctor.xml',
        # 'views/sale.xml',
        'data/sequence.xml',
        'data/data.xml',
        'reports/report.xml',
        'reports/patient_card.xml'
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
