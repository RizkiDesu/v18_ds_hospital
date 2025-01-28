from odoo import models, fields, api


class DsAsessment(models.Model):
    _name           = 'ds.nursing.assessment'
    _description    = 'Nursing Asessment'

    _inherit        = ['ds.hospital.library']

    # INHERITS Health Observation Services
    _inherits       = {'ds.observation.services': 'observation_id'}
    observation_id  = fields.Many2one('ds.observation.services', string='Registration', required=True, ondelete='cascade')


    chief_complaint             = fields.Text(string='Chief Complaint')
    family_history_of_illness   = fields.Text(string='Family history of illness')
    history_of_previous_illness = fields.Text(string='History of previous illness')
    history_of_allergies        = fields.Text(string='History of allergies')


    product_id                  = fields.Many2one('product.product', string='Product')



    def action_confirm(self):
        if not self.product_id :
            # product_id = id(self.env['ir.config_parameter'].sudo().get_param('ds_hospital_observation_services.nursing_assessment_product'))
            self.product_id = int(self.env['ir.config_parameter'].sudo().get_param('ds_hospital_observation_services.nursing_assessment_product'))     
        self.state = 'confirm'

    def action_done(self):
        self.state = 'done'

    def action_cancel(self):
        self.state = 'cancel'

    def action_draft(self):
        self.state = 'draft'

    def tesss(self):
        # print('tes')
        obj_observation               = self.env['ds.observation.services'].search([('registration_id', '=', self.registration_id.id)], limit=1, order='id desc')
        print(self.registration_id.name)
        print(obj_observation.name)

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
        # return rec