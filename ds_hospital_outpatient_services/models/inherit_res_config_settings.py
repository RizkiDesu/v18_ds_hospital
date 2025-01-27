from odoo import api, fields, models, _

class ResConfigSettings(models.TransientModel):
    _inherit                        = 'res.config.settings'


    registration_outpatient_service = fields.Many2one('ds.hospital.service', string='Registration Outpatient Service' , config_parameter='ds_hospital_outpatient_services.registration_outpatient_service')
    
    registration_outpatient_product = fields.Many2one('product.product', string='Registration Outpatient Product' , config_parameter='ds_hospital_outpatient_services.registration_outpatient_product')



    