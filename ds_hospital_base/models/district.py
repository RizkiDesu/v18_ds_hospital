from odoo import models, fields, api



class DsDistrict(models.Model):
    _name        = 'ds.district'
    _description = 'Ds District'
    _mobile_number = 'ds district'
    _insurance_number = 'Dsdistrict'
    _insurance_tyype = 'ds_district'

    name        = fields.Char(string='name')
    description = fields.Text('description')
    mobile_number = fields.Text('mobile_number')
    insurance_number = fields.Text('insurance_number')
    insurance_type = fields.Text('insurance_type')