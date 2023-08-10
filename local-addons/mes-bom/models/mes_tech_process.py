from odoo import models, fields, api


class TechSequence(models.Model):
    """Technological Sequence to be added"""
    _name = 'tech.sequence'
    _rec_name = 'order'

    order = fields.Integer(string='Order')


class TechProcess(models.Model):
    """TECHNICAL PROCESS"""
    _name = 'tech.process'
    _rec_name = 'name'
    _order = "sequence"

    name = fields.Char(string='Process Name*', required=True)
    code = fields.Char(string='Process Code')
    sequence = fields.Many2one('tech.sequence', string='Sequence')
    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Name must be unique!'),
        ('code_uniq', 'unique(code)', 'Code must be unique!')
    ]
    description = fields.Char(string='Process Description')
    bom_ids = fields.Many2many('mrp.bom', string='BOM')

    # For multiple level process
    parent_process = fields.Many2one('tech.process', string='Parent Process')
    child_process_ids = fields.One2many('tech.process',
                                        'parent_process',
                                        string='Child Process')

    # Process Line
    input = fields.One2many('material.line', 'tech_process_id',
                            string="Parent Input")
    input_description = fields.Html(string='Input Description')
    # Child Process Inputs and Combined Inputs
    child_process_inputs = fields.Many2many('material.line', compute='_compute_child_inputs', string='Child Inputs')
    combined_inputs = fields.Many2many('material.line', compute='_compute_combined_inputs', string='All Inputs')

    @api.depends('child_process_ids', 'child_process_ids.input')
    def _compute_child_inputs(self):
        def get_child_inputs(process, is_root=True):
            inputs = process.env['material.line']
            if not is_root:
                inputs = process.mapped('input')
            for child in process.child_process_ids:
                inputs |= get_child_inputs(child, is_root=False)
            return inputs

        for record in self:
            all_inputs = get_child_inputs(record)
            record.child_process_inputs = [(6, 0, all_inputs.ids)]

    @api.depends('input', 'child_process_inputs')
    def _compute_combined_inputs(self):
        for record in self:
            combined_inputs = record.input | record.child_process_inputs
            record.combined_inputs = [(6, 0, combined_inputs.ids)]

    # Machine Section
    machine = fields.One2many('equipment.usage', 'tech_process_id',
                              string="Parent Machine Usage")

    child_process_machines = fields.Many2many('equipment.usage', compute='_get_child_process_machines',
                                              string='Child Procss Machines')

    @api.depends('child_process_ids', 'child_process_ids.machine')
    def _get_child_process_machines(self):
        def get_child_machines(process, is_root=True):
            machines = process.env['equipment.usage']
            if not is_root:
                machines = process.mapped('machine')
            for child in process.child_process_ids:
                machines |= get_child_machines(child, is_root=False)
            return machines

        for record in self:
            all_machines = get_child_machines(record)
            record.child_process_machines = [(6, 0, all_machines.ids)]

    combined_machines = fields.Many2many('equipment.usage', compute='_compute_combined_machines', string='All Machines')

    @api.depends('machine', 'child_process_machines')
    def _compute_combined_machines(self):
        for record in self:
            combined_machines = record.mapped('machine') | record.child_process_machines
            record.combined_machines = [(6, 0, combined_machines.ids)]

    # MAN SECTION
    worker = fields.One2many('worker.type.usage', 'tech_process_id', string="Parent Worker Type")
    child_process_workers = fields.Many2many('worker.type.usage', compute='_compute_child_workers',
                                             string='Child Process Worker Type')
    combined_workers = fields.Many2many('worker.type.usage', compute='_compute_combined_workers',
                                        string='All Worker Type')

    @api.depends('child_process_ids', 'child_process_ids.worker')
    def _compute_child_workers(self):
        def get_child_workers(process, is_root=True):
            workers = process.env['worker.type.usage']
            if not is_root:
                workers = process.mapped('worker')
            for child in process.child_process_ids:
                workers |= get_child_workers(child, is_root=False)
            return workers

        for record in self:
            all_workers = get_child_workers(record)
            record.child_process_workers = [(6, 0, all_workers.ids)]

    @api.depends('worker', 'child_process_workers')
    def _compute_combined_workers(self):
        for record in self:
            combined_workers = record.worker | record.child_process_workers
            record.combined_workers = [(6, 0, combined_workers.ids)]

    # OUTPUT SECTION

    output = fields.One2many('output.line', 'tech_process_id',
                             string='Output')
    child_process_outputs = fields.Many2many('output.line', compute='_compute_child_outputs',
                                             string='Child Process Output')
    combined_outputs = fields.Many2many('output.line', compute='_compute_combined_outputs', string='All Output')

    @api.depends('child_process_ids', 'child_process_ids.output')
    def _compute_child_outputs(self):
        def get_child_outputs(process, is_root=True):
            outputs = process.env['output.line']
            if not is_root:
                outputs = process.mapped('output')
            for child in process.child_process_ids:
                outputs |= get_child_outputs(child, is_root=False)
            return outputs

        for record in self:
            all_outputs = get_child_outputs(record)
            record.child_process_outputs = [(6, 0, all_outputs.ids)]

    @api.depends('output', 'child_process_outputs')
    def _compute_combined_outputs(self):
        for record in self:
            combined_outputs = record.output | record.child_process_outputs
            record.combined_outputs = [(6, 0, combined_outputs.ids)]

    output_description = fields.Html(string='Output Description')
    image = fields.Image(string='Image')
    documents = fields.Binary(string='Document')
    document_name = fields.Char(string="File Name")
    ng_percent = fields.Float(string='% NG')


