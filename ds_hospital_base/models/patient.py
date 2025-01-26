from odoo import models, fields, api

class Patient(models.Model):
    _name           = 'ds.patient'
    _description    = 'Patient'

    # INHERITS RES PARTNER
    _inherits       = {'res.partner': 'partner_id'}
    partner_id      = fields.Many2one('res.partner', string='Patient', required=True, ondelete='cascade')

    @api.model
    def create(self, vals):
        res = super(Patient, self).create(vals)
        res.partner_id.write({'hospital_partner_type': 'patient', 'company_type': 'person', 'is_company': False})
        return res
    
    responsible_patient = fields.Many2one('res.partner', string='Responsible Patient', domain=[('company_type', '=', 'person')])