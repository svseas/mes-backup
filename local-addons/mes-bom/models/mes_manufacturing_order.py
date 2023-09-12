from odoo import fields, api, models, exceptions
from datetime import datetime


class ManufacturingOrderLine(models.Model):
    """MANUFACTURING ORDER LINE - Dòng lệnh sản xuất"""
    _name = 'mes.manufacturing.order.line'
    _rec_name = 'product'

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
    manufacturing_order_id = fields.Many2one('mes.manufacturing.order', string='Manufacturing Order', required=True)
    date_start = fields.Date(string='Date Start', required=True)
    date_end = fields.Date(string='Date End', required=True)

    # SQL Constraints to make sure date_end > date_start

    stock_entry_date = fields.Date(string='Stock Entry Date', required=True)
    delivery_date = fields.Date(string='Delivery Date', required=True)

    _sql_constraints = [
        ('date_check',
         'CHECK((date_end > date_start))',
         'Date end must be after date start.')
    ]


class DeliverySchedule(models.Model):
    """TO DO: MOVE THIS MODEL TO SALE ORDER LATER. Delivery Schedule - Tiến độ giao hàng"""
    _name = 'mes.delivery.schedule'

    manufacturing_order_id = fields.Many2one('mes.manufacturing.order', string='Manufacturing Order', required=True)
    product_id = fields.Many2one('product.product', string='Product', required=True,
                                 compute='_compute_product_id', store=True, readonly=False)

    @api.depends('manufacturing_order_id', 'manufacturing_order_id.manufacturing_order_line_ids.product')
    def _compute_product_id(self):
        for schedule in self:
            if schedule.manufacturing_order_id:
                product_ids = schedule.manufacturing_order_id.mapped('manufacturing_order_line_ids.product')
                if product_ids:
                    schedule.product_id = product_ids[0]
                else:
                    schedule.product_id = False
            else:
                schedule.product_id = False

    bom_id = fields.Many2one('mrp.bom', string='BOM', required=True,
                             compute='_compute_bom_id', store=True, readonly=False)

    @api.depends('product_id')
    def _compute_bom_id(self):
        for schedule in self:
            if schedule.product_id:
                bom = self.env['mrp.bom'].search([('product_tmpl_id', '=', schedule.product_id.product_tmpl_id.id)],
                                                 limit=1)
                if bom:
                    schedule.bom_id = bom
                else:
                    schedule.bom_id = False
            else:
                schedule.bom_id = False

    quantity = fields.Float(string='Quantity', required=True)
    uom = fields.Char(string='UOM', required=True)
    stock_entry_date = fields.Date(string='Stock Entry Date', required=True)
    delivery_date = fields.Date(string='Delivery Date', required=True)


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

    manufacturing_order_line_ids = fields.One2many('mes.manufacturing.order.line', 'manufacturing_order_id',
                                                   string='Manufacturing Order Lines')
    created_by = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user)
    approved_by = fields.Many2one('res.users', string='Approved By', default=lambda self: self.env.user)
    date_start = fields.Date(string='Date Start', required=True)
    date_end = fields.Date(string='Date End', required=True)

    contract_id = fields.Char(string='Contract ID')
    customer_id = fields.Many2one('res.partner', string='Customer')
    document = fields.Binary(string='Document')
    delivery_schedule_ids = fields.One2many('mes.delivery.schedule', 'manufacturing_order_id',
                                            string='Delivery Schedule')

    @api.constrains('date_start', 'date_end')
    def _check_date_start_end(self):
        for record in self:
            if record.date_start > record.date_end:
                raise exceptions.ValidationError('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')


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

    manufacturing_order_line_id = fields.Many2one('mes.manufacturing.order.line',
                                                  string="Manufacturing Order Line",
                                                  required=True)
    manufacturing_order_id = fields.Char(string="Manufacturing Order",
                                         related='manufacturing_order_line_id.manufacturing_order_id.name')
    workshop = fields.Many2one('mes.workshop', string="Workshop", required=True)
    product = fields.Many2one('product.product',
                              string="Product",
                              required=True)
    bom = fields.Many2one('mrp.bom', string="BOM", required=True)

    @api.onchange('manufacturing_order_line_id')
    def _onchange_manufacturing_order_line_id(self):
        """Change Product and BOM based on Manufacturing Order Line"""
        for rec in self:
            if rec.manufacturing_order_line_id:
                rec.product = rec.manufacturing_order_line_id.product
                rec.bom = rec.manufacturing_order_line_id.bom
            else:
                rec.product = False
                rec.bom = False

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
    machine_type = fields.Many2one('equipment.usage', string="Machine Type")
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
        """Set time_start and time_end to the same date as date_created"""
        for record in self:
            if record.date_created:
                # If time_start or time_end is not set, use a default time
                if not record.time_start:
                    record.time_start = datetime.combine(record.date_created,
                                                         datetime.min.time())  # Default to 00:00:00
                else:
                    record.time_start = record.time_start.replace(year=record.date_created.year,
                                                                  month=record.date_created.month,
                                                                  day=record.date_created.day)

                if not record.time_end:
                    record.time_end = datetime.combine(record.date_created, datetime.min.time())  # Default to 00:00:00
                else:
                    record.time_end = record.time_end.replace(year=record.date_created.year,
                                                              month=record.date_created.month,
                                                              day=record.date_created.day)

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
    manufacturing_order_line_id = fields.Many2one('mes.manufacturing.order.line', string="Manufacturing Order Line",
                                                  required=True)
    work_order_transition = fields.Many2one('mes.work.order', string="Work Order to Transit", required=True)
    work_order_receive = fields.Many2one('mes.work.order', string="Work Order to Receive", required=True)

    product = fields.Many2one('product.product', string="Product", required=True)
    bom = fields.Many2one('mrp.bom', string="BOM", required=True)

    @api.onchange('manufacturing_order_line_id')
    def _get_product_and_bom(self):
        """Get Product and BOM based on Manufacturing Order Line"""
        for record in self:
            if record.manufacturing_order_line_id:
                record.product = record.manufacturing_order_line_id.product
                record.bom = record.manufacturing_order_line_id.bom
            else:
                record.product = False
                record.bom = False

    @api.onchange('manufacturing_order_line_id')
    def _onchange_manufacturing_order_line_id(self):
        """Change Work Order Transition and Work Order Receive based on Manufacturing Order Line"""
        if self.manufacturing_order_line_id:
            domain = [('manufacturing_order_line_id', '=', self.manufacturing_order_line_id.id)]
            work_orders = self.env['mes.work.order'].search(domain)
            self.work_order_transition = False
            self.work_order_receive = False
            return {'domain': {'work_order_transition': [('id', 'in', work_orders.ids)],
                               'work_order_receive': [('id', 'in', work_orders.ids)]}}

    shift = fields.Selection(
        selection=[('shift_1', 'Shift 1'),
                   ('shift_2', 'Shift 2'),
                   ('shift_3', 'Shift 3'),
                   ('shift_4', 'Shift 4')],
        string="Shift", required=True)

    created_by = fields.Many2one('res.users', string="Created By", default=lambda self: self.env.user)
    approved_by = fields.Many2one('res.users', string="Approved By", default=lambda self: self.env.user)
    transition_process = fields.Many2one('tech.process', string="Transition Process", store=True)

    @api.onchange('work_order_transition')
    def _compute_transition_process(self):
        """Get transition process based on work order transition"""
        for rec in self:
            if rec.work_order_transition:
                rec.transition_process = rec.work_order_transition.process
            else:
                rec.transition_process = False

    transition_quantity = fields.Float(string="Transition Quantity", required=True, default=1.00)
    receive_quantity = fields.Float(string="Receive Quantity", required=True, default=1.00)

    @api.constrains('transition_quantity')
    def _check_transition_quantity(self):
        for rec in self:
            if rec.transition_quantity <= 0:
                raise exceptions.ValidationError('Transition quantity must be greater than 0.')

    uom = fields.Char(string="UOM", required=True)
    reception_process = fields.Many2one('tech.process', string="Reception Process", required=True)

    @api.constrains('transition_process', 'reception_process', 'bom')
    def _check_processes_belong_to_bom(self):
        for rec in self:
            if rec.bom:
                # Get the processes related to the selected BOM
                domain = [('bom_ids', '=', rec.bom.id)]
                processes = rec.env['tech.process'].search(domain)

                # Check if the selected processes belong to the BOM
                if rec.transition_process not in processes or rec.reception_process not in processes:
                    raise exceptions.ValidationError(
                        'The Transition Process and Reception Process must belong to the selected BOM.')

    @api.onchange('transition_process')
    def _onchange_transition_process(self):
        """Select Reception Process based on Transition Process"""
        for rec in self:
            if rec.transition_process and rec.bom:
                next_order = rec.transition_process.sequence.order + 1
                next_process = rec.env['tech.process'].search([
                    ('sequence.order', '=', next_order),
                    ('bom_ids', '=', rec.bom.id)
                ], limit=1)
                if next_process:
                    rec.reception_process = next_process.id
                else:
                    rec.reception_process = False
                return {'domain': {'reception_process': [('id', '=', rec.reception_process.id)]}}

    @api.onchange('reception_process')
    def _onchange_reception_process(self):
        """Select Work Order Receive based on reception process"""
        for rec in self:
            if rec.reception_process:
                domain = [('process', '=', rec.reception_process.id)]
                work_orders = rec.env['mes.work.order'].search(domain)
                rec.work_order_receive = False
                return {'domain': {'work_order_receive': [('id', 'in', work_orders.ids)]}}

    transistor = fields.Many2one('res.users', string="Transistor", default=lambda self: self.env.user)
    receptor = fields.Many2one('res.users', string="Receptor", default=lambda self: self.env.user)

    @api.onchange('work_order_transition')
    def _onchange_work_order_transition(self):
        """Change transistor based on Work Order Transition"""
        for rec in self:
            if rec.work_order_transition:
                rec.transistor = rec.work_order_transition.worker_ids.id
            else:
                rec.transistor = False

    @api.onchange('work_order_receive')
    def _onchange_work_order_receive(self):
        """Change receptor based on Work Order Receive"""
        for rec in self:
            if rec.work_order_receive:
                rec.receptor = rec.work_order_receive.worker_ids.id
            else:
                rec.receptor = False

    reception_quantity = fields.Float(string="Reception Quantity", required=True, default=1.00)
    quality_control_line = fields.One2many('quality.control.line', 'work_transition_id', string="Quality Control Line")

    @api.constrains('reception_quantity')
    def _check_reception_quantity(self):
        for rec in self:
            if rec.reception_quantity <= 0:
                raise exceptions.ValidationError('Reception quantity must be greater than 0.')

    ng_redo_transit = fields.Float(string="NG Redo Transit", required=True)
    ng_not_redo_transit = fields.Float(string="NG Not Redo", required=True)
    ng_redo_receive = fields.Float(string="NG Redo Receive", required=True)
    ng_not_redo_receive = fields.Float(string="NG Not Redo Receive", required=True)
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

    class QualityControlLine(models.Model):
        _name = "quality.control.line"
        _description = "Quality Control Line"

        reception_quantity = fields.Float(string="Reception Quantity", required=True)
        ng_redo = fields.Float(string="NG Redo", required=True)
        ng_not_redo = fields.Float(string="NG Not Redo", required=True)
        uom = fields.Char(string="UOM", required=True)
        work_transition_id = fields.Many2one('mes.work.transition', string="Work Transition", ondelete='cascade')
