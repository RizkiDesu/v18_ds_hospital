from odoo import api, fields, models, _
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
from datetime import datetime
from odoo import Command
import base64
from io import BytesIO



class DsHospitalLibrary(models.AbstractModel):
    _name = "ds.hospital.library"
    _description = "Hospital Library"
            
    def ds_create_invoice(self, invoice_data):
        """Method for creating invoice"""
        invoice_vals = {
            'move_type'         : 'out_invoice',
            'date'              : fields.Date.today(),
            'invoice_date'      : fields.Date.today(),
            'partner_id'        : invoice_data['partner_id'],
            'partner_ids'       : invoice_data['partner_ids'] or [],
            'invoice_line_ids'  : [],
        }
        for line in invoice_data['product_ids']:
            invoice_line_vals = {
                'product_id'    : line['product_id'],
                'quantity'      : line['quantity'],
                'price_unit'    : line['price_unit'],
            }
            invoice_vals['invoice_line_ids'].append((0, 0, invoice_line_vals))
        invoice_id = self.env['account.move'].sudo().create(invoice_vals)
        return invoice_id
            
        