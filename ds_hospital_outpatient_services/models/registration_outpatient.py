from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError



class DsRegistrationOutpatient(models.Model):
    _name           = 'ds.registration.outpatient'
    _description    = 'Registration Outpatient'

    _inherit        = ['ds.hospital.library']

    # INHERITS Health Registration
    _inherits            = {'ds.health.registration': 'registration_id'}
    registration_id      = fields.Many2one('ds.health.registration', string='Registration', required=True, ondelete='cascade')

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
        rec = super().default_get(fields_list)
        rec['service_id'] = int(self.env['ir.config_parameter'].sudo().get_param('ds_hospital_outpatient_services.registration_outpatient_service'))
        rec['product_service_id'] = int(self.env['ir.config_parameter'].sudo().get_param('ds_hospital_outpatient_services.registration_outpatient_product'))
        return rec
    
    @api.onchange('doctor_id', 'nurse_id', 'midwife_id')
    def _onchange_doctor_id(self):
        self.health_workers_ids = False
        health_workers_ids = []
        if self.doctor_id:
            health_workers_ids.append((4, self.doctor_id.id))
        if self.nurse_id:
            health_workers_ids.append((4, self.nurse_id.id))
        if self.midwife_id:
            health_workers_ids.append((4, self.midwife_id.id))
        self.health_workers_ids = health_workers_ids

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
                'quantity'      : 1,
                'price_unit'    : self.product_service_id.list_price
            })
        if not self.invoice_id:
            if self.product_service_id != False:
                invoice_id = self.ds_create_invoice({
                    'partner_id'    : self.patient_id.partner_id.id,
                    'partner_ids'   : partner_ids,
                    'product_ids'   : product_ids
                })
                self.invoice_id = invoice_id

        self.state = 'confirm'
    def action_cancel(self):
        if self.invoice_id:
            self.invoice_id.action_cancel()
        self.state = 'cancel'

        

        
