from odoo import models, fields, api



class DsVillage(models.Model):
    _name = 'ds.village'
    _description = 'Ds Village'
    _mobile_number = 'ds village'
    _insurance_number = 'Dsvillage'
    _insurance_tyype = 'ds_village'

    name = fields.Char(string='name')
    description = fields.Text('description')
    mobile_number = fields.Text('mobile_number')
    insurance_number = fields.Text('insurance_number')
    insurance_type = fields.Text('insurance_type')
    
