from odoo import models, fields, api

class DsCity(models.Model):
    _name        = 'ds.city'
    _description = 'Ds City'
    _mobile_number = 'ds city'
    _insurance_number = 'Dscity'
    _insurance_tyype = 'ds_city'

    name        = fields.Char(string='name')
    description = fields.Text('description')
    mobile_number = fields.Text('mobile_number')
    insurance_number = fields.Text('insurance_number')
    insurance_type = fields.Text('insurance_type')