from odoo import models, fields, api

class DsHospitalService(models.Model):
    _name           = 'ds.hospital.service'
    _description    = 'Hospital Service'

    name            = fields.Char(string='Name', required=True)
    code            = fields.Char(string='Code')
    description     = fields.Text(string='Description')

    hospital_id     = fields.Many2one(comodel_name='res.company', string='Hospital')

    service_lines   = fields.One2many(comodel_name='ds.hospital.service.line', inverse_name='service_id', string='Service Lines')
    

class DsHospitalServiceLine(models.Model):
    _name               = 'ds.hospital.service.line'
    _description        = 'Hospital Service Line'

    name                = fields.Char(string='Name')
    code                = fields.Char(string='Code')
    description         = fields.Text(string='Description')
    service_id          = fields.Many2one(comodel_name='ds.hospital.service', string='Service')

    product_service_ids = fields.One2many(comodel_name='product.template', inverse_name='hospital_service_id', string='Product Services')
    




