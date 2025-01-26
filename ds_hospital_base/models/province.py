from odoo import models, fields, api

class DsProvince(models.Model):
    _name        = 'ds.province'
    _description = 'Ds Province'

    name        = fields.Char(string='name')
    description = fields.Text('description')
    