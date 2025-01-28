from odoo import models, fields, api



class DsPatient(models.Model):
    _inherit                    = 'ds.patient'
    observasion_services_ids    = fields.One2many(comodel_name='ds.observation.services', inverse_name='patient_id', string='Observation Services')
    

class DsObservationService(models.Model):
    _name               = 'ds.observation.services'
    _description        = 'Observation Services'


    name                = fields.Char(string='Name')
    diagnosis_id        = fields.Many2one(comodel_name='ds.icd10', string='Diagnosis')


    STATE_OBSERVATION_SERVICES = [
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('cancel', 'Cancel'),
        ('done', 'Done'),
    ]

    state               = fields.Selection(string='State', selection=STATE_OBSERVATION_SERVICES, default='draft')
    
    date_time_create    = fields.Datetime(string='Date Time Create', default=fields.Datetime.now)
    
    registration_id     = fields.Many2one(comodel_name='ds.health.registration', string='Registration')
    
    REQ_TYPE            = []
    req_type            = fields.Selection(string='Registration Type', selection=REQ_TYPE)

    patient_id          = fields.Many2one(comodel_name='ds.patient', string='Patient')
    mr_number           = fields.Char(related='patient_id.mr_number', string='MR Number', store=True)
    
    service_id          = fields.Many2one(comodel_name='ds.hospital.service', string='Service')
    service_line_id     = fields.Many2one(comodel_name='ds.hospital.service.line', string='Service Line')
    specialist_id       = fields.Many2one(comodel_name='ds.specialist', string='Specialist', related='service_line_id.specialist_id', store=True)
    is_midwifery        = fields.Boolean(string='Midwifery', related='service_line_id.is_midwifery', store=True)
    doctor_id           = fields.Many2one(comodel_name='hr.employee', string='Doctor')
    nurse_id            = fields.Many2one(comodel_name='hr.employee', string='Nurse')
    midwife_id          = fields.Many2one(comodel_name='hr.employee', string='Midwife')
    health_workers_ids  = fields.Many2many(comodel_name='hr.employee', string='Health Workers')
    partner_ids         = fields.Many2many(comodel_name='res.partner', string='Partners')

    weight              = fields.Float(string='Body Weight', help="Body Weight in KG")
    height              = fields.Float(string='Height', help="Height in cm")
    temp                = fields.Float(string='Body Temperature', help='Body Temperature')
    hr                  = fields.Float(string='Heart Rate', help="Heart Rate")
    rr                  = fields.Float(string='Resp. Rate', help='Respiratory Rate')
    systolic_bp         = fields.Float("Systolic BP")
    diastolic_bp        = fields.Float("Diastolic BP")
    spo2                = fields.Float(string='SpO2', help='Oxygen Saturation, percentage of oxygen bound to hemoglobin')

    consciousness       = fields.Selection(string='level of consciousness', selection=[('alert', 'Alert'), ('v_p_u', 'V/P/U')], default='alert') 
    @api.depends('height', 'weight')
    def get_bmi_data(self):
        for rec in self:
            bmi = 0
            bmi_state = False
            if rec.height and rec.weight:
                try:
                    bmi = float(rec.weight) / ((float(rec.height) / 100) ** 2)
                except:
                    bmi = 0
                bmi_state = 'normal'
                if bmi < 18.5:
                    bmi_state = 'low_weight'
                elif 25 < bmi < 30:
                    bmi_state = 'over_weight'
                elif bmi > 30:
                    bmi_state = 'obesity'
            rec.bmi = bmi
            rec.bmi_state = bmi_state

    BMI_STATE = [
        ('low_weight', 'Low Weight'), 
        ('normal', 'Normal'),
        ('over_weight', 'Ovew Weight'), 
        ('obesity', 'Obesity')
        ]
    
    bmi             = fields.Float(compute="get_bmi_data", string='Body Mass Index', store=True)
    bmi_state       = fields.Selection(BMI_STATE, compute="get_bmi_data", string='BMI State', store=True)
    gcs_input       = fields.Char(string='GCS (E,M,V)')
    gcs_score       = fields.Integer(string='Score GCS')

    
    product_id      = fields.Many2one('product.product', string='Product')

    chief_complaint             = fields.Text(string='Chief Complaint')
    family_history_of_illness   = fields.Text(string='Family history of illness')
    history_of_previous_illness = fields.Text(string='History of previous illness')
    history_of_allergies        = fields.Text(string='History of allergies')

    @api.model
    def create(self, vals):
        res = super(DsObservationService, self).create(vals)
        sequence = self.env['ir.sequence'].next_by_code('ds.observation')
        res.write({
            'name': sequence
        })
        return res