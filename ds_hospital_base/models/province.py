from odoo import models, fields, api

class DsProvince(models.Model):
    _name        = 'ds.province'
    _description = 'Ds Province'
    _mobile_number = 'ds province'
    _insurance_number = 'Dsprovince'
    _insurance_tyype = 'ds_province'

    name        = fields.Char(string='name')
    description = fields.Text('description')
    mobile_number = fields.Text('mobile_number')
    insurance_number = fields.Text('insurance_number')
    insurance_type = fields.Text('insurance_type')
    