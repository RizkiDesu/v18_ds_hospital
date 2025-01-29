from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError



class DsMedicalTreatmentOutpatient(models.Model):
    _inherit = 'ds.medical.treatment'
    REQ_TYPE = [
        ('outpatient', 'Outpatient'),
        ]
    req_type = fields.Selection(string='Registration Type', selection_add=REQ_TYPE)

class DsInspectionOutpatient(models.Model):
    _inherit = 'ds.inspection'
    REQ_TYPE = [
        ('outpatient', 'Outpatient'),
        ]
    req_type = fields.Selection(string='Registration Type', selection_add=REQ_TYPE)

class DsObservationServicesOutpatient(models.Model):
    _inherit = 'ds.observation.services'

    REQ_TYPE = [
        ('outpatient', 'Outpatient'),
        ]
    req_type = fields.Selection(string='Registration Type', selection_add=REQ_TYPE)

class DsHealthRegistrationOutpatient(models.Model):
    _inherit = 'ds.health.registration'
    REQ_TYPE = [
        ('outpatient', 'Outpatient'),
        ]
    req_type = fields.Selection(string='Registration Type', selection_add=REQ_TYPE)

class DsRegistrationOutpatient(models.Model):
    _name           = 'ds.registration.outpatient'
    _description    = 'Registration Outpatient'

    _inherit        = ['ds.hospital.library']

    # INHERITS Health Registration
    _inherits       = {'ds.health.registration': 'registration_id'}
    registration_id = fields.Many2one('ds.health.registration', string='Registration', required=True, ondelete='cascade')

    @api.model
    def create(self, vals):
        res = super(DsRegistrationOutpatient, self).create(vals)
        sequence = self.env['ir.sequence'].next_by_code('ds.oupatient')
        res.registration_id.write(
            {
             'name': sequence,
             })
        return res
    @api.model
    def default_get(self, fields_list):
        rec                         = super().default_get(fields_list)
        rec['req_type']             = 'outpatient'
        rec['service_id']           = int(self.env['ir.config_parameter'].sudo().get_param('ds_hospital_outpatient_services.registration_outpatient_service'))
        rec['product_service_id']   = int(self.env['ir.config_parameter'].sudo().get_param('ds_hospital_outpatient_services.registration_outpatient_product'))
        return rec
    
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

    def action_confirm(self):
        if not self.service_line_id:
            raise UserError(_('Unit Layanan belum terdefinisi !'))
        if len(self.health_workers_ids) == 0:
            raise UserError(_('health workers have not yet been filled !'))
        partner_ids = []
        product_ids = []
        if self.doctor_id:
            partner_ids.append((4, self.doctor_id.work_contact_id.id))
        if self.nurse_id:
            partner_ids.append((4, self.nurse_id.work_contact_id.id))
        if self.midwife_id:
            partner_ids.append((4, self.midwife_id.work_contact_id.id))
        if self.product_service_id:
            product_ids.append({
                'product_id'    : self.product_service_id.id,
                'qty'      : 1,
                'price'    : self.product_service_id.list_price
                
            })
        if not self.invoice_id:
            if self.product_service_id != False:
                invoice_id = self.ds_create_invoice({
                    'partner_id'        : self.patient_id.partner_id.id,
                    'partner_ids'       : partner_ids,
                    'product_ids'       : product_ids,
                    'registration_id'   : self.registration_id.id
                })
                self.invoice_id = invoice_id
        self.state          = 'confirm'
        
    def action_cancel(self):
        if self.invoice_id:
            self.invoice_id.button_cancel()
        self.state = 'cancel'

    @api.onchange('patient_id')
    def _onchange_patient_id(self):
        if self.patient_id:
            self.responsible_patient = self.patient_id.responsible_patient
        else:
            self.responsible_patient = False
    
    def action_nursing_assessment(self):
        action = self.env["ir.actions.actions"]._for_xml_id("ds_hospital_observation_services.ds_nursing_assessment_action")
        action['domain'] = [('registration_id', '=', self.registration_id.id), ('req_type', '=', self.req_type)]
        action['context'] = {
            'default_registration_id': self.registration_id.id, 
            'default_req_type' : self.req_type, 
            'default_patient_id' : self.patient_id.id,
            'default_doctor_id' : self.doctor_id.id,
            'default_nurse_id' : self.nurse_id.id,
            'default_midwife_id' : self.midwife_id.id,
            'default_service_id' : self.service_id.id,
            'default_service_line_id' : self.service_line_id.id,
        }     
        return action
    

    def action_medical_assessment(self):
        action = self.env["ir.actions.actions"]._for_xml_id("ds_hospital_observation_services.ds_medical_assessment_action")
        action['domain'] = [('registration_id', '=', self.registration_id.id), ('req_type', '=', self.req_type)]
        action['context'] = {
            'default_registration_id': self.registration_id.id, 
            'default_req_type' : self.req_type, 
            'default_patient_id' : self.patient_id.id,
            'default_doctor_id' : self.doctor_id.id,
            'default_nurse_id' : self.nurse_id.id,
            'default_midwife_id' : self.midwife_id.id,
            'default_service_id' : self.service_id.id,
            'default_service_line_id' : self.service_line_id.id,
        }
                             
        return action
    def action_inspection(self):
        action = self.env["ir.actions.actions"]._for_xml_id("ds_hospital_observation_services.ds_inspection_action")
        action['domain'] = [('registration_id', '=', self.registration_id.id), ('req_type', '=', self.req_type)]
        action['context'] = {
            'default_registration_id': self.registration_id.id, 
            'default_req_type' : self.req_type, 
            'default_patient_id' : self.patient_id.id,
            'default_doctor_id' : self.doctor_id.id,
            'default_nurse_id' : self.nurse_id.id,
            'default_midwife_id' : self.midwife_id.id,
            'default_service_id' : self.service_id.id,
            'default_service_line_id' : self.service_line_id.id,
        }
                             
        return action
    def action_medical_treatment(self):
        action = self.env["ir.actions.actions"]._for_xml_id("ds_hospital_observation_services.ds_medical_treatment_action")
        action['domain'] = [('registration_id', '=', self.registration_id.id), ('req_type', '=', self.req_type)]
        action['context'] = {
            'default_registration_id': self.registration_id.id, 
            'default_req_type' : self.req_type, 
            'default_patient_id' : self.patient_id.id,
            'default_doctor_id' : self.doctor_id.id,
            'default_nurse_id' : self.nurse_id.id,
            'default_midwife_id' : self.midwife_id.id,
            'default_service_id' : self.service_id.id,
            'default_service_line_id' : self.service_line_id.id,
        }
                             
        return action

        

        
