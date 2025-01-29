from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    HOSPITAL_PRODUCT_TYPE = [
        ('rooms','Rooms'),
        ('consultation','Consultasion'),
        ('service','Service')
    ]
    hospital_product_type = fields.Selection(string='Hospital Product Type', selection=HOSPITAL_PRODUCT_TYPE)
    service_id          = fields.Many2one(comodel_name='ds.hospital.service', string='Service')
    hospital_service_id = fields.Many2one(comodel_name='ds.hospital.service.line', string='Service')
    
    