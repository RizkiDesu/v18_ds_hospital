from odoo import models, fields, api

class DsCity(models.Model):
    _name        = 'ds.city'
    _description = 'Ds City'

    name        = fields.Char(string='name')
    description = fields.Text('description')
    
