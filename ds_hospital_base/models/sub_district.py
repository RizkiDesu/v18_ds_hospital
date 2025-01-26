from odoo import models, fields, api

class DsSubdistrict(models.Model):
    _name        = 'ds.sub_district'
    _description = 'Ds Subdistrict'

    name        = fields.Char(string='name')
    description = fields.Text('description')