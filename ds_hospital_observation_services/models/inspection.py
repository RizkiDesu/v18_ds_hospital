from odoo import models, fields, api

class DsInspection(models.Model):
    _name               = 'ds.inspection'
    _description        = 'Inspection'

    name                = fields.Char(string='Name')

    diagnosis_id        = fields.Many2one(comodel_name='ds.icd10', string='Diagnosis')
    @api.model
    def create(self, vals):
        res = super(DsInspection, self).create(vals)
        sequence = self.env['ir.sequence'].next_by_code('ds.inspection')
        res.write({
            'name': sequence
        })
        return res
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

    def action_confirm(self):
        if not self.product_id :
            self.product_id = int(self.env['ir.config_parameter'].sudo().get_param('ds_hospital_observation_services.inspection_product'))     
        self.state = 'confirm'

    def action_done(self):
        self.state = 'done'

    def action_cancel(self):
        self.state = 'cancel'

    def action_draft(self):
        self.state = 'draft'
    

    @api.onchange('patient_id')
    def _onchange_patient_id(self):
        if self.registration_id:
            obj_observation               = self.env['ds.observation.services'].search([('patient_id', '=', self.patient_id.id)], limit=1, order='id desc')
            if obj_observation:
                self.systolic_bp    = obj_observation.systolic_bp
                self.diastolic_bp   = obj_observation.diastolic_bp
                self.rr             = obj_observation.rr
                self.hr             = obj_observation.hr
                self.temp           = obj_observation.temp
                self.weight         = obj_observation.weight
                self.height         = obj_observation.height
                self.spo2           = obj_observation.spo2
                self.gcs_score      = obj_observation.gcs_score
                self.consciousness  = obj_observation.consciousness
            else:
                self.systolic_bp    = 0
                self.diastolic_bp   = 0
                self.rr             = 0
                self.hr             = 0
                self.temp           = 0
                self.weight         = 0
                self.height         = 0
                self.spo2           = 0
                self.gcs_score      = 0
                self.consciousness  = 'alert'