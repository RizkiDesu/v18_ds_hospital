from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    HOSPITAL_PRODUCT_TYPE = [
        ('treatment','Treatment'),
        ('drug','Drug')
    ]
    hospital_product_type = fields.Selection(selection_add=HOSPITAL_PRODUCT_TYPE)
    ds_bundle_product_ids = fields.One2many(
        comodel_name='ds.product.bundle',
        inverse_name='ds_bundle_id',
        string="Bundle Line",copy=True, auto_join=True)
    ds_is_bundle = fields.Boolean('Is Bundled ?')
    ds_amount_total = fields.Monetary(
        string='Total', store=True, readonly=True, compute='_compute_amount_all')

    @api.depends('ds_bundle_product_ids.ds_price_subtotal')
    def _compute_amount_all(self):
        amount_total = 0.0
        for order in self:
            if order.ds_bundle_product_ids:
                for line in order.ds_bundle_product_ids:
                    amount_total += line.ds_price_subtotal
                order.ds_amount_total = amount_total

    def compute_bundle_price(self):
        list_price = 0.0
        if self.ds_bundle_product_ids:
            for bundle_product in self.ds_bundle_product_ids:
                list_price += bundle_product.ds_price_subtotal
        self.list_price = list_price

    def compute_bundle_cost_price(self):
        standard_price = 0.0
        if self.ds_bundle_product_ids:
            for bundle_product in self.ds_bundle_product_ids:
                standard_price += (bundle_product.ds_cost_price *
                                   bundle_product.ds_qty)
        self.standard_price = standard_price


class Product(models.Model):
    _inherit = 'product.product'

    def compute_bundle_price(self):
        lst_price = 0.0
        if self.ds_bundle_product_ids:
            for bundle_product in self.ds_bundle_product_ids:
                lst_price += bundle_product.ds_price_subtotal
        self.lst_price = lst_price

    def compute_bundle_cost_price(self):
        standard_price = 0.0
        if self.ds_bundle_product_ids:
            for bundle_product in self.ds_bundle_product_ids:
                standard_price += (bundle_product.ds_cost_price *
                                   bundle_product.ds_qty)
        self.standard_price = standard_price


class DsBundleProduct(models.Model):
    _name = 'ds.product.bundle'
    _description = 'Bundle Products'

    # def _product_id_domain(self):
    # # employee_ids is considered a safe field and as such will be fetched as sudo.
    # # So try to enforce the security rules on the field to make sure we do not load employees outside of active companies
    #     print('\n\n SELF',self)
    #     return [('id', '!=', self.ds_bundle_id.product_variant_id.id)]

    ds_bundle_id = fields.Many2one('product.template', 'Bundle ID')
    ds_product_id = fields.Many2one(
        'product.product', 'Product', required=True)
    ds_qty = fields.Float("Quantity")
    ds_uom = fields.Many2one('uom.uom', 'Unit of Measure', required=True)
    ds_price_unit = fields.Float('Unit Price')
    ds_cost_price = fields.Float(related="ds_product_id.standard_price")
    ds_price_subtotal = fields.Float('Sub Total', readonly=True, store=True)

    @api.onchange('ds_product_id')
    def _onchange_ds_product_id(self):
        if self.ds_product_id:
            self.ds_uom = self.ds_product_id.uom_id.id
            self.ds_qty = 1.0
            self.ds_price_unit = self.ds_product_id.list_price

    @api.onchange('ds_qty', 'ds_price_unit')
    def get_price_subtotal(self):
        for rec in self:
            rec.ds_price_subtotal = rec.ds_price_unit * rec.ds_qty
    


class DsMedicalTreatment(models.Model):
    _name           = 'ds.medical.treatment'
    _description    = 'Medical Treatment'
    _inherit        = ['ds.hospital.library']


    name            = fields.Char(string='Name')
    @api.model
    def create(self, vals):
        res = super(DsMedicalTreatment, self).create(vals)
        sequence = self.env['ir.sequence'].next_by_code('ds.treatment')
        res.write({
            'name': sequence
        })
        return res
    STATE_OBSERVATION_SERVICES = [
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('cancel', 'Cancel'),
        ('done', 'Done'),
    ]
    state               = fields.Selection(string='State', selection=STATE_OBSERVATION_SERVICES, default='draft')
    date_time_create    = fields.Datetime(string='Date Time Create', default=fields.Datetime.now)
    registration_id     = fields.Many2one(comodel_name='ds.health.registration', string='Registration')
    REQ_TYPE            = []
    req_type            = fields.Selection(string='Registration Type', selection=REQ_TYPE)

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
    partner_ids         = fields.Many2many(comodel_name='res.partner', string='Partners')
    # stock_move_id       = fields.Many2one(comodel_name='stock.move', string='Stock Move')
    def action_confirm(self):

        if len(self.treatment_ids) > 0 and self.treatment_ids:
            product_ids = []
            for treatment in self.treatment_ids:
                product_ids.append({
                    'product_id'    : treatment.product_id.id,
                    'qty'           : treatment.qty,
                    'price'         : treatment.price
                })

            if not self.invoice_id:
                invoice_id = self.ds_create_invoice({
                    'partner_id'        : self.patient_id.partner_id.id,
                    'partner_ids'       : self.partner_ids,
                    'product_ids'       : product_ids,
                    'registration_id'   : self.registration_id.id
                })
                self.invoice_id = invoice_id
                # self.ds_stock_reduction_list(self.treatment_ids)
                for line in self.treatment_ids:
                    consu = self.ds_stock_reduction({
                        'product_id'    : line.product_id,
                        'qty'           : line.qty
                    })

        self.state = 'confirm'

    def action_done(self):
        self.state = 'done'

    def action_cancel(self):
        self.state = 'cancel'

    def action_draft(self):
        self.state = 'draft'

    treatment_ids = fields.One2many(comodel_name='ds.medical.treatment.line', inverse_name='treatment_id', string='Treatment Lines')
    invoice_id  = fields.Many2one(comodel_name='account.move', string='Invoice')
class DsMedicalTreatmentLine(models.Model):
    _name           = 'ds.medical.treatment.line'
    _description    = 'Medical Treatment Line'

    treatment_id    = fields.Many2one(comodel_name='ds.medical.treatment', ondelete='cascade', string='Treatment', required=True, index=True)
    product_id      = fields.Many2one(comodel_name='product.product', ondelete='restrict', string='Item Treatment', required=True)
    qty             = fields.Float(string='Jumlah', required=True)
    price           = fields.Float(string='Price', required=True)
    total           = fields.Float(string='Total', compute='_compute_total', store=True)
    description     = fields.Char(string='Description')

    @api.depends('qty', 'price')
    def _compute_total(self):
        for r in self:
            r.total = r.qty * r.price

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.price = self.product_id.lst_price
            self.qty = 1
            self.total = self.price * self.qty

    @api.onchange('qty')
    def _onchange_qty(self):
        if self.qty:
            self.total = self.price * self.qty
    
    @api.onchange('price')
    def _onchange_harga(self):
        if self.price:
            self.total = self.price * self.qty


    