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

    def get_combined_inputs(self, bom):
        # Compute combined inputs for the given BOM
        # Return the combined inputs as a Many2many recordset
        combined_inputs = self.combined_inputs
        # Implement the logic to compute combined inputs based on the BOM
        return combined_inputs

    @api.depends('bom_tech_process_ids')
    def _compute_combined_processes(self):
        for record in self:
            combined_processes = record.bom_tech_process_ids
            record.combined_processes = combined_processes

    @api.depends('bom')
    def _compute_combined_inputs(self):
        for record in self:
            if record.bom:
                combined_inputs = record.bom.tech_process_id.get_combined_inputs(record.bom)
                record.combined_inputs = combined_inputs

