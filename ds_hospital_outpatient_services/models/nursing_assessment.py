from odoo import api, fields, models, _

class DsNursingAssessmentOutpatient(models.Model):
    _inherit = 'ds.nursing.assessment'


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