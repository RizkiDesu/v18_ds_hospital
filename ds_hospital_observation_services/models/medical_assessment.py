from odoo import models, fields, api

class DsMedicalAssessment(models.Model):
    _name           = 'ds.medical.assessment'
    _description    = 'Medical Assessment'

    _inherit        = ['ds.hospital.library']

    # INHERITS Health Observation Services
    _inherits       = {'ds.observation.services': 'observation_id'}
    observation_id  = fields.Many2one('ds.observation.services', string='Registration', required=True, ondelete='cascade')  

    def action_confirm(self):
        if not self.product_id :
            # product_id = id(self.env['ir.config_parameter'].sudo().get_param('ds_hospital_observation_services.nursing_assessment_product'))
            self.product_id = int(self.env['ir.config_parameter'].sudo().get_param('ds_hospital_observation_services.medical_assessment_product'))     
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
                self.diagnosis_id   = obj_observation.diagnosis_id
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
                
    @api.onchange('doctor_id', 'nurse_id', 'midwife_id')
    def _onchange_doctor_id(self):
        self.health_workers_ids = False
        health_workers_ids      = []
        partner_ids             = []
        if self.doctor_id:
            health_workers_ids.append((4, self.doctor_id.id))
            partner_ids.append((4, self.doctor_id.work_contact_id.id))
        if self.nurse_id:
            health_workers_ids.append((4, self.nurse_id.id))
            partner_ids.append((4, self.nurse_id.work_contact_id.id))
        if self.midwife_id:
            health_workers_ids.append((4, self.midwife_id.id))
            partner_ids.append((4, self.midwife_id.work_contact_id.id))
        self.health_workers_ids = health_workers_ids
        self.partner_ids        = partner_ids