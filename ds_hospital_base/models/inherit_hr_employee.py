from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit                        = 'res.partner'
    SELECTION_TYPE                  = [('doctor', 'Doctor'), ('nurse', 'Nurse'),('midwife', 'Midwife')]
    hospital_partner_type           = fields.Selection(selection_add=SELECTION_TYPE)
    is_health_workers               = fields.Boolean(string='Health Workers')

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    PARTNER_TYPE                    = [('employee', 'Employee'),('doctor', 'Doctor'), ('nurse', 'Nurse'),('midwife', 'Midwife'),('other', 'Other')]
    hospital_partner_type           = fields.Selection(string='Hospital Type', selection=PARTNER_TYPE, default='employee')

    identity_card                   = fields.Char(string='Identity card Number') # KTP
    insurance_number                = fields.Char(string='Insurance Number') # ASURANSI
    
    INSURANCE_TYPE                  = [('independent', 'Independent'),('insured', 'Insured')]
    insurance_type                  = fields.Selection(string='Insurance Type', selection=INSURANCE_TYPE, default='independent', required=True)
    
    birth_date                      = fields.Date(string='Birth Date')
    gender                          = fields.Selection(string='Gender', selection=[('male', 'Male'), ('female', 'Female')])
    is_health_workers               = fields.Boolean(string='Health Workers')
    
    @api.onchange('hospital_partner_type')
    def _onchange_hospital_partner_type(self):
        self.work_contact_id.hospital_partner_type  = self.hospital_partner_type
        self.work_contact_id.identity_card          = self.identity_card
        self.work_contact_id.insurance_type         = self.insurance_type
        self.work_contact_id.insurance_number       = self.insurance_number
        self.work_contact_id.birth_date             = self.birth_date
        self.work_contact_id.gender                 = self.gender
        self.work_contact_id.is_health_workers      = self.is_health_workers







