# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Bom(models.Model):
    _inherit = ['mrp.bom']

    tech_process_ids = fields.Many2many('tech.process',
                                        string='Technical Process')
    ng_percent = fields.Float(string='NG Percent*',
                              required=True,
                              default=0)
    created_by = fields.Many2one('res.users',
                                 string='Created By*',
                                 required=True)
    approved_by = fields.Many2one('res.users',
                                  string='Approved By*',
                                  required=True)
    bom_uom = fields.Char(string='UOM', help="Unit of measurement")

    # Combined inputs to show in BOM
    combined_inputs = fields.Many2many('material.line', compute='_get_combined_inputs', string='Materials Used')
    combined_machines = fields.Many2many('equipment.usage', compute='_get_combined_machines', string='Machines Used')
    combined_workers = fields.Many2many('worker.type.usage', compute='_get_combined_workers', string='Man Used')

    @api.depends('tech_process_ids', 'tech_process_ids.combined_inputs')
    def _get_combined_inputs(self):
        for record in self:
            # get all combined_inputs from tech.process and combine them
            combined_inputs = record.mapped('tech_process_ids.combined_inputs')
            # Assign the combined inputs to the field
            record.combined_inputs = [(6, 0, combined_inputs.ids)]

    @api.depends('tech_process_ids', 'tech_process_ids.combined_machines')
    def _get_combined_machines(self):
        for record in self:
            # get all combined_inputs from tech.process and combine them
            combined_machines = record.mapped('tech_process_ids.combined_machines')
            # Assign the combined inputs to the field
            record.combined_machines = [(6, 0, combined_machines.ids)]

    @api.depends('tech_process_ids', 'tech_process_ids.combined_workers')
    def _get_combined_workers(self):
        for record in self:
            # get all combined_inputs from tech.process and combine them
            combined_workers = record.mapped('tech_process_ids.combined_workers')
            # Assign the combined inputs to the field
            record.combined_workers = [(6, 0, combined_workers.ids)]
