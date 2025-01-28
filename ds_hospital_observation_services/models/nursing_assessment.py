from odoo import models, fields, api


class DsAsessment(models.Model):
    _name           = 'ds.nursing.assessment'
    _description    = 'Nursing Asessment'

    _inherit        = ['ds.hospital.library']

    # INHERITS Health Observation Services
    _inherits       = {'ds.observation.services': 'observation_id'}
    observation_id  = fields.Many2one('ds.observation.services', string='Registration', required=True, ondelete='cascade')

