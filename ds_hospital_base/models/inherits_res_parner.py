from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit    = 'res.partner'

    identity_card       = fields.Char(string='Identity card Number') # KTP
    insurance_number    = fields.Char(string='Insurance Number') # ASURANSI
    
    INSURANCE_TYPE      = [('independent', 'Independent'),('insured', 'Insured')]
    insurance_type      = fields.Selection(string='Insurance Type', selection=INSURANCE_TYPE, default='independent', required=True)
    
    
