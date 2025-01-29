from odoo import api, fields, models, _

class ResConfigSettings(models.TransientModel):
    _inherit                        = 'res.config.settings'


    nursing_assessment_product = fields.Many2one('product.product', string='Registration Outpatient Product' , config_parameter='ds_hospital_observation_services.nursing_assessment_product')
    medical_assessment_product = fields.Many2one('product.product', string='Medical Assessment Product' , config_parameter='ds_hospital_observation_services.medical_assessment_product')
    inspection_product         = fields.Many2one('product.product', string='Inspection' , config_parameter='ds_hospital_observation_services.inspection_product') 