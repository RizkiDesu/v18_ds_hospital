from odoo import models, fields, api



class DsDistrict(models.Model):
    _name        = 'ds.district'
    _description = 'Ds District'

    name        = fields.Char(string='name')
    description = fields.Text('description')
    
