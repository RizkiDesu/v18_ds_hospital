from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    auto_invoice                    = fields.Boolean(string='Invoice Not Draft', config_parameter='ds_hospital_base.auto_invoice')
    appointment_usage_location_id   = fields.Many2one('stock.location', domain  = [('usage','=','customer')],string  = 'Location Stock for Appointment', config_parameter='ds_hospital_base.appointment_usage_location_id')
    appointment_stock_location_id   = fields.Many2one('stock.location', domain  = [('usage','=','internal')],string  = 'Stock Location for Consumed Products in Appointment', config_parameter='ds_hospital_base.appointment_stock_location_id')