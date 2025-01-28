from odoo import models, fields, api


# READONLY_STATES = {'draft': [('readonly', False)], 'confirm': [('readonly', True)],'process': [('readonly', True)], 'cancel': [('readonly', True)], 'done': [('readonly', True)]}
class DsHealthRegistration(models.Model):
    _name               = 'ds.health.registration'
    _description        = 'Health Registration'


    name                = fields.Char(string='Name')
    diagnosis_id        = fields.Many2one(comodel_name='ds.icd10', string='Diagnosis')
    
    date_time_create    = fields.Datetime(string='Date Time Create', default=fields.Datetime.now)
    REQ_TYPE            = []
    req_type            = fields.Selection(string='Registration Type', selection=REQ_TYPE)
    
    patient_id          = fields.Many2one(comodel_name='ds.patient', string='Patient')
    mr_number           = fields.Char(related='patient_id.mr_number', string='MR Number', store=True)

    identity_card       = fields.Char(string='Identity card Number', related='patient_id.identity_card', store=True)
    birth_date          = fields.Date(string='Birth Date', related='patient_id.birth_date', store=True)
    gender              = fields.Selection(string='Gender', related='patient_id.gender', store=True)

    INSURANCE_TYPE      = [('independent', 'Independent'),('insured', 'Insured')]
    insurance_type      = fields.Selection(string='Insurance Type', selection=INSURANCE_TYPE, default='independent', required=True)
    insurance_number    = fields.Char(string='Insurance Number')

    @api.onchange('patient_id')
    def _onchange_patient_id(self):
        if self.patient_id:
            self.insurance_type     = self.patient_id.insurance_type
            self.insurance_number   = self.patient_id.insurance_number

    
    service_id          = fields.Many2one(comodel_name='ds.hospital.service', string='Service')
    service_line_id     = fields.Many2one(comodel_name='ds.hospital.service.line', string='Service Line')
    specialist_id       = fields.Many2one(comodel_name='ds.specialist', string='Specialist', related='service_line_id.specialist_id', store=True)
    
    is_midwifery        = fields.Boolean(string='Midwifery', related='service_line_id.is_midwifery', store=True)
    
    doctor_id           = fields.Many2one(comodel_name='hr.employee', string='Doctor')
    nurse_id            = fields.Many2one(comodel_name='hr.employee', string='Nurse')
    midwife_id          = fields.Many2one(comodel_name='hr.employee', string='Midwife')
    health_workers_ids  = fields.Many2many(comodel_name='hr.employee', string='Health Workers')
    partner_ids         = fields.Many2many(comodel_name='res.partner', string='Partners')

    product_service_id  = fields.Many2one(comodel_name='product.product', string='Product Service')
    invoice_id          = fields.Many2one(comodel_name='account.move', string='Invoice')

    STATES_HEALTH_REGISTRASION = [
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('process', 'Process'),
        ('done', 'Done'),
        ('cancel', 'Cancel'),
        ]
    
    state               = fields.Selection(string='State', selection=STATES_HEALTH_REGISTRASION, default="draft")
    
    responsible_patient = fields.Many2one('res.partner', string='Responsible Patient', domain=[('company_type', '=', 'person')])

    

    


