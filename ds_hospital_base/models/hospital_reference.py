from odoo import models, fields, api
from odoo.osv import expression


class DsSpecialist(models.Model):
    _name           = 'ds.specialist'
    _description    = 'Specialist'

    name            = fields.Char(string='name')
    code            = fields.Char(string='code')
    description     = fields.Text(string='Description')


class DsIcd10(models.Model):
    _name           = 'ds.icd10'
    _description    = 'Icd10'

    name            = fields.Char(string='name')
    code            = fields.Char(string='code')
    description     = fields.Text(string='Description')


class DsIcd9(models.Model):
    _name           = 'ds.icd9'
    _description    = 'Icd9'

    name            = fields.Char(string='name')
    code            = fields.Char(string='code')
    description     = fields.Text(string='Description')

