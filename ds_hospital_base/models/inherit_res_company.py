from odoo import models, fields, api

class ResCompany(models.Model):
    _inherit = 'res.company'

    service_ids     = fields.One2many(comodel_name='ds.hospital.service', inverse_name='hospital_id', string='Hospital Services')





