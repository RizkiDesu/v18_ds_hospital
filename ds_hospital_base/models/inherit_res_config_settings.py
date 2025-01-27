from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    auto_invoice        = fields.Boolean(string='Invoice Not Draft', config_parameter='ds_hospital_base.auto_invoice')



    