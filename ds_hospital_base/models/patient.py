from odoo import models, fields, api

class Patient(models.Model):
    _name                           = 'ds.patient'
    _description                    = 'Patient'

    # INHERITS RES PARTNER
    _inherits                       = {'res.partner': 'partner_id'}
    partner_id                      = fields.Many2one('res.partner', string='Patient', required=True, ondelete='cascade')
    def action_view_partner_invoices(self):
        return self.partner_id.action_view_partner_invoices()
    @api.model
    def create(self, vals):
        res = super(Patient, self).create(vals)
        sequence_mr = self.env['ir.sequence'].next_by_code('ds.medical.record')
        res.partner_id.write(
            {'hospital_partner_type': 'patient', 
             'company_type': 'person', 
             'is_company': False,
             'mr_number': sequence_mr,
             })
        return res
    
    responsible_patient             = fields.Many2one('res.partner', string='Responsible Patient', domain=[('company_type', '=', 'person')])
    
    history_hospital_registration   = fields.One2many(comodel_name='ds.health.registration', inverse_name='patient_id', string='History Hospital Registration', domain=[('state','=','done')])