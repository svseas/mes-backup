from odoo import fields, api, models, exceptions


class ManufacturingOrder(models.Model):
    """MANUFACTURING ORDER - Lệnh sản xuất"""
    _name = 'mes.manufacturing.order'
    _rec_name = 'code'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True)

    @api.constrains('name', 'code')
    def _check_name_and_code(self):
        for record in self:
            if record.name == record.code:
                raise exceptions.ValidationError('The name and code must be different.')

    @api.constrains('name')
    def _check_name_unique(self):
        for record in self:
            if self.env['mes.manufacturing.order'].search_count([('name', '=', record.name)]) > 1:
                raise exceptions.ValidationError('The name must be unique.')

    @api.constrains('code')
    def _check_code_unique(self):
        for record in self:
            if self.env['mes.manufacturing.order'].search_count([('code', '=', record.code)]) > 1:
                raise exceptions.ValidationError('The code must be unique.')

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

    # SQL Constraints to make sure date_end > date_start
    _sql_constraints = [
        ('date_check',
         'CHECK((date_end > date_start))',
         'The end date must be after the start date.')
    ]
    contract_id = fields.Char(string='Contract ID')
    customer_id = fields.Many2one('res.partner', string='Customer')
    document = fields.Binary(string='Document')


class WorkShop(models.Model):
    """Workshop - Xưởng sản xuất"""

    _name = "mes.workshop"
    _rec_name = "name"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)

    @api.constrains('name', 'code')
    def _check_name_and_code(self):
        for record in self:
            if record.name == record.code:
                raise exceptions.ValidationError('The name and code must be different.')

    @api.constrains('name')
    def _check_name_unique(self):
        for record in self:
            if self.env['mes.workshop'].search_count([('name', '=', record.name)]) > 1:
                raise exceptions.ValidationError('The name must be unique.')

    @api.constrains('code')
    def _check_code_unique(self):
        for record in self:
            if self.env['mes.workshop'].search_count([('code', '=', record.code)]) > 1:
                raise exceptions.ValidationError('The code must be unique.')


class ProductivityReport(models.Model):
    _name = 'productivity.report'
    _rec_name = 'work_order_id'

    shift = fields.Selection(
        selection=[('shift_1', 'Shift 1'),
                   ('shift_2', 'Shift 2'),
                   ('shift_3', 'Shift 3'),
                   ('shift_4', 'Shift 4')],
        string="Shift", required=True)
    quantity = fields.Float(string='Quantity')
    work_order_id = fields.Many2one('mes.work.order', string='Work Order')


class WorkOrder(models.Model):
    """Work Order - Phiếu giao việc"""

    _name = "mes.work.order"
    _rec_name = "code"

    code = fields.Char(string="Code", required=True)

    @api.constrains('code')
    def _check_code_unique(self):
        for record in self:
            if self.env['mes.work.order'].search_count([('code', '=', record.code)]) > 1:
                raise exceptions.ValidationError('The code must be unique.')

    manufacturing_id = fields.Many2one('mes.manufacturing.order', string="Manufacturing Order", required=True)
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

    sfg = fields.Many2one('output.line', string="Semi-Finished Goods", required=True)

    @api.onchange('process')
    def _onchange_process(self):
        """Select SFG based on process"""
        if self.process:
            domain = [('tech_process_id', '=', self.process.id)]
            sfgs = self.env['output.line'].search(domain)
            self.sfg = False
            return {'domain': {'sfg': [('id', 'in', sfgs.ids)]}}

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

    @api.onchange('date_created')
    def _onchange_date_created(self):
        for rec in self:
            if rec.date_created:
                date_created = fields.Date.from_string(rec.date_created)
                if rec.time_start:
                    time_start = fields.Datetime.from_string(rec.time_start)
                    rec.time_start = fields.Datetime.to_string(
                        datetime.datetime.combine(date_created, time_start.time())
                    )
                if rec.time_end:
                    time_end = fields.Datetime.from_string(rec.time_end)
                    rec.time_end = fields.Datetime.to_string(
                        datetime.datetime.combine(date_created, time_end.time())
                    )

    _sql_constraints = [
        ('time_check',
         'CHECK((time_end > time_start))',
         'The end time must be after the start time.')
    ]

    quantity = fields.Float(string="Quantity", required=True)
    quantity_new = fields.Float(string="Quantity New", required=True)
    quantity_redo = fields.Float(string="Quantity Redo", required=True)
    uom = fields.Char(string="UOM", required=True)
    status = fields.Selection(
        selection=[('draft', 'Draft'), ('confirmed', 'Confirmed'), ('in_progress', 'In Progress'), ('done', 'Done')],
        default='draft')

    productivity_report = fields.One2many('productivity.report', 'work_order_id', string='Productivity Report')


class WorkTransition(models.Model):
    """Work Transition - Phiếu chuyển tiếp"""

    _name = "mes.work.transition"
    _rec_name = "code"

    code = fields.Char(string="Code", required=True)

    @api.constrains('code')
    def _check_code_unique(self):
        for record in self:
            if self.env['mes.work.transition'].search_count([('code', '=', record.code)]) > 1:
                raise exceptions.ValidationError('The code must be unique.')

    workshop = fields.Many2one('mes.workshop', string="Workshop", required=True)
    manufacturing_order = fields.Many2one('mes.manufacturing.order', string="Manufacturing Order", required=True)
    product = fields.Many2one('product.product', string="Product", required=True)

    @api.onchange('manufacturing_order')
    def _onchange_manufacturing_order(self):
        """Update Product when manufacturing order is changed"""
        if self.manufacturing_order:
            domain = [('product_tmpl_id', '=', self.manufacturing_order.product.product_tmpl_id.id)]
            products = self.env['product.product'].search(domain)
            self.product = False  # Clear the product field
            return {'domain': {'product': [('id', 'in', products.ids)]}}

    bom = fields.Many2one('mrp.bom', string="BOM", required=True)

    shift = fields.Selection(
        selection=[('shift_1', 'Shift 1'),
                   ('shift_2', 'Shift 2'),
                   ('shift_3', 'Shift 3'),
                   ('shift_4', 'Shift 4')],
        string="Shift", required=True)

    @api.onchange('product')
    def _onchange_product(self):
        """Update bom domain when product is changed to show only boms related to the product"""
        if self.product:
            domain = [('product_tmpl_id', '=', self.product.product_tmpl_id.id)]
            boms = self.env['mrp.bom'].search(domain)
            self.bom = False
            return {'domain': {'bom': [('id', 'in', boms.ids)]}}

    created_by = fields.Many2one('res.users', string="Created By", default=lambda self: self.env.user)
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

    transition_quantity = fields.Float(string="Transition Quantity", required=True, default=1.00)

    @api.constrains('transition_quantity')
    def _check_transition_quantity(self):
        for rec in self:
            if rec.transition_quantity <= 0:
                raise exceptions.ValidationError('Transition quantity must be greater than 0.')

    uom = fields.Char(string="UOM", required=True)
    reception_process = fields.Many2one('tech.process', string="Reception Process", required=True)

    @api.onchange('transition_process')
    def _onchange_transition_process(self):
        """Select Reception Process based on Transition Process"""
        if self.transition_process and self.bom:
            next_order = self.transition_process.sequence.order + 1
            next_process = self.env['tech.process'].search([
                ('sequence.order', '=', next_order),
                ('bom_ids', '=', self.bom.id)
            ], limit=1)
            if next_process:
                self.reception_process = next_process.id
            else:
                self.reception_process = False
            return {'domain': {'reception_process': [('id', '=', self.reception_process.id)]}}

    receptor = fields.Many2one('res.users', string="Receptor", default=lambda self: self.env.user)
    reception_quantity = fields.Float(string="Reception Quantity", required=True, default=1.00)

    @api.constrains('reception_quantity')
    def _check_reception_quantity(self):
        for rec in self:
            if rec.reception_quantity <= 0:
                raise exceptions.ValidationError('Reception quantity must be greater than 0.')

    ng_redo = fields.Float(string="NG Redo", required=True)
    ng_not_redo = fields.Float(string="NG Not Redo", required=True)
    documents = fields.Binary(string="Documents")
    document_name = fields.Char(string="Document Name")
    activity_log_ids = fields.One2many('mes.work.transition.activity.log', 'work_transition_id', string="Activity Log")

    class WorkTransitionActivityLog(models.Model):
        _name = "mes.work.transition.activity.log"
        _description = "Work Transition Activity Log"
        _rec_name = "activity_date"

        activity_date = fields.Datetime(string="Activity Date", default=fields.Datetime.now, required=True)
        user_id = fields.Many2one('res.users', string="User", default=lambda self: self.env.user, required=True)
        description = fields.Text(string="Description", required=True)
        work_transition_id = fields.Many2one('mes.work.transition', string="Work Transition", ondelete='cascade')
