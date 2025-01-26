from odoo import models, fields, api

class DsSubdistrict(models.Model):
    _name        = 'ds.sub_district'
    _description = 'Ds Subdistrict'
    _mobile_number = 'ds sub_district'
    _insurance_number = 'Dssub_district'
    _insurance_tyype = 'ds_sub_district'

    name        = fields.Char(string='name')
    description = fields.Text('description')
    mobile_number = fields.Text('mobile_number')
    insurance_number = fields.Text('insurance_number')
    insurance_type = fields.Text('insurance_type')