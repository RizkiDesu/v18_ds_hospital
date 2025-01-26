from odoo import models, fields, api

class Patient(models.Model):
    _name           = 'ds.patient'
    _description    = 'Patient'

    # INHERITS RES PARTNER
    _inherits       = {'res.partner': 'partner_id'}
    partner_id      = fields.Many2one('res.partner', string='Patient', required=True, ondelete='cascade')
