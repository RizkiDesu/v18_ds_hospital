from odoo import models, fields, api



class DsHealthRegistration(models.Model):
    _name               = 'ds.health.registration'
    _description        = 'Health Registration'


    name                = fields.Char(string='Name')
    diagnosis_id        = fields.Many2one(comodel_name='ds.icd10', string='Diagnosis')

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

    product_service_id  = fields.Many2one(comodel_name='product.product', string='Product Service')
    invoice_id       = fields.Many2one(comodel_name='account.move', string='Invoice')

    STATES_HEALTH_REGISTRASION = [
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('process', 'Process'),
        ('done', 'Done'),
        ('cancel', 'Cancel'),
        ]
    
    state = fields.Selection(string='State', selection=STATES_HEALTH_REGISTRASION, default="draft")
    


    


