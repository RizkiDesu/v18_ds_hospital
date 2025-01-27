from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    partner_ids = fields.Many2many(comodel_name='res.partner', string='Health Workers')
    