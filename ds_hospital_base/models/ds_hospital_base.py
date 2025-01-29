from odoo import api, fields, models, _
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
from datetime import datetime
from odoo import Command
import base64
from io import BytesIO

class DsHospitalLibrary(models.AbstractModel):
    _name           = "ds.hospital.library"
    _description    = "Hospital Library"
            

    
    def ds_create_invoice(self, invoice_data):
        """Method for creating invoice"""
        invoice_vals = {
            'move_type'         : 'out_invoice',
            'date'              : fields.Date.today(),
            'invoice_date'      : fields.Date.today(),
            'partner_id'        : invoice_data['partner_id'],
            'partner_ids'       : invoice_data['partner_ids'] or [],
            'registration_id'   : invoice_data['registration_id'] or False,
            'invoice_line_ids'  : [],
        }
        for line in invoice_data['product_ids']:
            invoice_line_vals = {
                'product_id'    : line['product_id'],
                'quantity'      : line['qty'],
                'price_unit'    : line['price'],
            }
            invoice_vals['invoice_line_ids'].append((0, 0, invoice_line_vals))
        invoice_id      = self.env['account.move'].sudo().create(invoice_vals)
        invoice_id._onchange_partner_id()
        auto_invoice    = self.env['ir.config_parameter'].sudo().get_param('ds_hospital_base.auto_invoice')
        if auto_invoice == 'True' or auto_invoice == True:
            invoice_id.action_post()
        return invoice_id

            
    def ds_stock_reduction(self, product_data):
        """Method for stock reduction"""
        source_location_id  = int(self.env['ir.config_parameter'].sudo().get_param('ds_hospital_base.appointment_stock_location_id')) or False
        dest_location_id    = int(self.env['ir.config_parameter'].sudo().get_param('ds_hospital_base.appointment_usage_location_id')) or False
        if not dest_location_id:
            raise UserError(_('Please set the Material Usage Location in the Hospital Configuration menu'))
        if not source_location_id:
            raise UserError(_('Please set the Stock Material Location in the Hospital Configuration menu'))
        product             = product_data['product_id']
        # --------------------------- START FOR BUNDLE PRODUCT ---------------------------
        # move = False
        if product.ds_is_bundle:
            for bundle_item in product.ds_bundle_product_ids:
                if product.is_storable:
                    data = {
                        'name'              : bundle_item.ds_product_id.name,
                        'product_id'        : bundle_item.ds_product_id.id,
                        'product_uom'       : bundle_item.ds_uom.id,
                        'product_uom_qty'   : bundle_item.ds_qty or 1.0,
                        'date'              : product_data.get('date', fields.datetime.now()),
                        'location_id'       : source_location_id,
                        'location_dest_id'  : dest_location_id,
                        'state'             : 'draft',
                        'origin'            : self.name,
                        'quantity_done'     : bundle_item.ds_qty or 1.0,
                    }
                    move = self.env['stock.move'].create(data)
                    move._action_confirm()
                    move._action_assign()
                    if product_data.get('lot_id'):
                        lot_id  = product_data['lot_id']
                        lot_qty = bundle_item.ds_qty or 1.0
                        self.assign_given_lots(move, lot_id, lot_qty)
                    if move.state == 'assigned':
                        move._action_done()
        # --------------------------- END FOR BUNDLE PRODUCT ---------------------------

        # --------------------------- START FOR SINGLE PRODUCT ---------------------------
        if product.is_storable:
            move = self.env['stock.move'].create({
                'name'              : product.name,
                'product_id'        : product.id,
                'product_uom'       : product.uom_id.id,
                'product_uom_qty'   : product_data.get('qty',1.0),
                'date'              : product_data.get('date',fields.datetime.now()),
                'location_id'       : source_location_id,
                'location_dest_id'  : dest_location_id,
                'state'             : 'draft',
                'origin'            : self.name,
                'quantity_done'     : product_data.get('qty',1.0),
            })
            move._action_confirm()
            move._action_assign()
            if product_data.get('lot_id', False):
                lot_id  = product_data.get('lot_id')
                lot_qty = product_data.get('qty',1.0)
                self.sudo().assign_given_lots(move, lot_id, lot_qty)
            if move.state == 'assigned':
                move._action_done()
            # --------------------------- END FOR SINGLE PRODUCT ---------------------------
            return move
    

    def ds_stock_reduction_list(self, product_ids):
        for product in product_ids:
            self.ds_stock_reduction(product)