from odoo import models, fields, api


class ManufacturingOrder(models.Model):
    """Manufacturing Order"""
    _name = 'mes.manufacturing.order'
    _rec_name = 'name'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True)
    product = fields.Many2one('product.product', string='Product', required=True)
    bom = fields.Many2one('mrp.bom', string='BOM', required=True)
    quantity = fields.Float(string='Quantity*', required=True, default=1.0)
    uom = fields.Char(string='UOM', required=True)
    created_by = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user)
    approved_by = fields.Many2one('res.users', string='Approved By', default=lambda self: self.env.user)
    date_start = fields.Date(string='Date Start', required=True)
    date_end = fields.Date(string='Date End', required=True)
    contract_id = fields.Char(string='Contract ID')
    customer_id = fields.Many2one('res.partner', string='Customer')
    document = fields.Binary(string='Document')
    bom_tech_process_ids = fields.Many2many(related='bom.tech_process_ids', string='BOM Tech Processes')

    combined_inputs = fields.Many2many('material.line', compute='_compute_combined_inputs', string='Combined Inputs')
    combined_machines = fields.Many2many('equipment.usage', compute='_compute_combined_machines',
                                         string='Combined Machines')
    combined_workers = fields.Many2many('worker.type.usage', compute='_compute_combined_workers',
                                        string='Combined Workers')
    combined_processes = fields.Many2many('tech.process', compute='_compute_combined_processes',
                                          string='Combined Processes')

    @api.depends('bom_tech_process_ids')
    def _compute_combined_processes(self):
        for record in self:
            combined_processes = record.bom_tech_process_ids
            record.combined_processes = combined_processes

    @api.depends('bom', 'bom.combined_inputs')
    def _compute_combined_inputs(self):
        for record in self:
            if record.bom:
                record.combined_inputs = record.bom.combined_inputs

    @api.depends('bom', 'bom.combined_machines')
    def _compute_combined_machines(self):
        for record in self:
            if record.bom:
                record.combined_machines = record.bom.combined_machines

    @api.depends('bom', 'bom.combined_workers')
    def _compute_combined_workers(self):
        for record in self:
            if record.bom:
                record.combined_workers = record.bom.combined_workers
