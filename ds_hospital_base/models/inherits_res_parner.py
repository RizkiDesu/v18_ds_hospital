from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit    = 'res.partner'

    identity_card                   = fields.Char(string='Identity card Number') # KTP
    insurance_number                = fields.Char(string='Insurance Number') # ASURANSI
    
    INSURANCE_TYPE                  = [('independent', 'Independent'),('insured', 'Insured')]
    insurance_type                  = fields.Selection(string='Insurance Type', selection=INSURANCE_TYPE, default='independent', required=True)
    
    PARTNER_TYPE                    = [('employee', 'Employee'), ('patient', 'Patient'),('other', 'Other')]
    hospital_partner_type           = fields.Selection(string='Type', selection=PARTNER_TYPE)
    
    mr_number                       = fields.Char(string='Medical Record Number')
    
