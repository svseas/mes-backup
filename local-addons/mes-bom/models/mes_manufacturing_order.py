from odoo import models, fields, api


class ManufacturingOrder(models.Model):
    """Manufacturing Order"""
    _name = 'mes.manufacturing.order'
    _rec_name = 'name'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True)
    product = fields.Many2one('product.product', string='Product', required=True)
    bom = fields.Many2one('mrp.bom', string='BOM', required=True)

    @api.onchange('product')
    def _onchange_product(self):
        if self.product:
            domain = [('product_tmpl_id', '=', self.product.product_tmpl_id.id)]
            boms = self.env['mrp.bom'].search(domain)
            self.bom = False  # Clear the bom field
            return {'domain': {'bom': [('id', 'in', boms.ids)]}}

    quantity = fields.Float(string='Quantity*', required=True, default=1.0)
    uom = fields.Char(string='UOM', required=True)
    created_by = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user)
    approved_by = fields.Many2one('res.users', string='Approved By', default=lambda self: self.env.user)
    date_start = fields.Date(string='Date Start', required=True)
    date_end = fields.Date(string='Date End', required=True)
    contract_id = fields.Char(string='Contract ID')
    customer_id = fields.Many2one('res.partner', string='Customer')
    document = fields.Binary(string='Document')
    # bom_tech_process_ids = fields.Many2many(related='bom.tech_process_ids', string='BOM Tech Processes')
    #
    # combined_inputs = fields.Many2many(related='bom.combined_inputs', string='Combined Inputs')


class WorkShop(models.Model):
    """Workshop - Xưởng sản xuất"""

    _name = "mes.workshop"
    _rec_name = "name"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)


class WorkOrder(models.Model):
    """Work Order - Phiếu giao việc"""

    _name = "mes.work.order"
    _rec_name = "code"

    code = fields.Char(string="Code", required=True)
    workshop = fields.Many2one('mes.workshop', string="Workshop", required=True)
    product = fields.Many2one('product.product', string="Product", required=True)
    bom = fields.Many2one('mrp.bom', string="BOM", required=True)

    @api.onchange('product')
    def _onchange_product(self):
        """Update bom domain when product is changed to show only boms related to the product"""
        if self.product:
            domain = [('product_tmpl_id', '=', self.product.product_tmpl_id.id)]
            boms = self.env['mrp.bom'].search(domain)
            self.bom = False  # Clear the bom field
            return {'domain': {'bom': [('id', 'in', boms.ids)]}}

    process = fields.Many2one('tech.process', string="Process", required=True)

    @api.onchange('bom')
    def _onchange_bom(self):
        """Select Process based on bom"""
        if self.bom:
            domain = [('bom_ids', '=', self.bom.id)]
            processes = self.env['tech.process'].search(domain)
            self.process = False  # Clear the process field
            return {'domain': {'process': [('id', 'in', processes.ids)]}}

    sfg = fields.Many2one('material.material', string="Semi-Finished Goods", required=True)
    created_by = fields.Many2one('res.users', string="Created By", default=lambda self: self.env.user)
    approved_by = fields.Many2one('res.users', string="Approved By", default=lambda self: self.env.user)
    documents = fields.Binary(string="Documents")
    document_name = fields.Char(string="Document Name")
    machine_type = fields.Many2one('equipment.template', string="Machine")
    machine = fields.Char(string="Machine")
    worker_type = fields.Many2one('worker.group', string="Worker Type")
    worker_ids = fields.Many2many('res.users', string="Worker List")

    @api.onchange('worker_type')
    def _onchange_worker_type(self):
        """Select Worker List based on Worker Type"""
        if self.worker_type:
            self.worker_ids = False  # Clear the worker_ids field
            return {'domain': {'worker_ids': [('id', 'in', self.worker_type.worker_ids.ids)]}}

    date_created = fields.Date(string="Date Created", required=True)
    time_start = fields.Datetime(string="Time Start", required=True)
    time_end = fields.Datetime(string="Time End", required=True)
    quantity = fields.Float(string="Quantity", required=True)
    quantity_new = fields.Float(string="Quantity New", required=True)
    quantity_redo = fields.Float(string="Quantity Redo", required=True)
    uom = fields.Char(string="UOM", required=True)
    status = fields.Selection(
        selection=[('draft', 'Draft'), ('confirmed', 'Confirmed'), ('in_progress', 'In Progress'), ('done', 'Done')],
        default='draft')


class WorkTransition(models.Model):
    """Work Transition - Phiếu chuyển tiếp"""

    _name = "mes.work.transition"
    _rec_name = "code"

    code = fields.Char(string="Code", required=True)
    workshop = fields.Many2one('mes.workshop', string="Workshop", required=True)
    manufacturing_order = fields.Many2one('mes.manufacturing.order', string="Manufacturing Order", required=True)
    product = fields.Many2one('product.product', string="Product", required=True)

    @api.onchange('manufacturing_order')
    def _onchange_product(self):
        """Update Product when manufacturing order is changed"""
        if self.manufacturing_order:
            domain = [('product_tmpl_id', '=', self.manufacturing_order.product.product_tmpl_id.id)]
            products = self.env['product.product'].search(domain)
            self.product = False  # Clear the product field
            return {'domain': {'product': [('id', 'in', products.ids)]}}

    bom = fields.Many2one('mrp.bom', string="BOM", required=True)

    @api.onchange('product')
    def _onchange_product(self):
        """Update bom domain when product is changed to show only boms related to the product"""
        if self.product:
            domain = [('product_tmpl_id', '=', self.product.product_tmpl_id.id)]
            boms = self.env['mrp.bom'].search(domain)
            self.bom = False
            return {'domain': {'bom': [('id', 'in', boms.ids)]}}

    shift = fields.Selection(selection=[('morning', 'Morning'), ('afternoon', 'Afternoon'), ('night', 'Night')],
                             string="Shift", required=True)

    approved_by = fields.Many2one('res.users', string="Approved By", default=lambda self: self.env.user)
    transition_process = fields.Many2one('tech.process', string="Transition Process", required=True)

    @api.onchange('bom')
    def _onchange_bom(self):
        """Select Process based on bom"""
        if self.bom:
            domain = [('bom_ids', '=', self.bom.id)]
            processes = self.env['tech.process'].search(domain)
            self.transition_process = False  # Clear the process field
            return {'domain': {'transition_process': [('id', 'in', processes.ids)]}}

    transition_quantity = fields.Float(string="Transition Quantity", required=True)
    uom = fields.Char(string="UOM", required=True)
    reception_process = fields.Many2one('tech.process', string="Reception Process", required=True)

    @api.onchange('transition_process')
    def _onchange_transition_process(self):
        """Select Reception Process based on Transition Process"""
        if self.transition_process:
            next_sequence = self.transition_process.sequence.sequence + 1
            next_process = self.env['tech.process'].search([('sequence', '=', next_sequence)], limit=1)
            if next_process:
                self.reception_process = next_process.id
            else:
                self.reception_process = False

    receptionist = fields.Many2one('res.users', string="Receptionist", default=lambda self: self.env.user)
    reception_quantity = fields.Float(string="Reception Quantity", required=True)
    ng_redo = fields.Float(string="NG Redo", required=True)
    ng_not_redo = fields.Float(string="NG Not Redo", required=True)
    documents = fields.Binary(string="Documents")
    document_name = fields.Char(string="Document Name")
