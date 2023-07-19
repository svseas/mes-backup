# -*- coding: utf-8 -*-

from odoo import models, fields, api


#TO DO
#REFACTOR WORKER INTO DIFFERENT ADD-ON: MES-WORKER
class MrpWorkerGroup(models.Model):
    """Worker Group for BOM and other modules in MRP"""
    _name = 'worker.group'
    _rec_name = 'name'

    name = fields.Char(string='Group Name')
    code = fields.Char(string='Group Code')
    expertise_level = fields.Selection(selection=[('type_one', 'Type 1'),
                                                  ('type_two', 'Type 2'),
                                                  ('type_three', 'Type 3')])
    capacity = fields.Float(string='Capacity',
                            help='Capacity is in hours')
    worker_ids = fields.Many2many('res.users',
                                  string="Worker List")
    bom_id = fields.Many2one('mrp.bom', string='BOM')
    tech_process_id = fields.Many2one('tech.process', string='Technical Stage')


class ProductProducts(models.Model):
    _inherit = 'product.product'

    tech_process_id = fields.Many2one('tech.process', string='Tech Process')

class TechSequence(models.Model):
    """Technological Sequence to be added"""
    _name = 'tech.sequence'
    _rec_name = 'order'

    order = fields.Integer(string='Order')


class TechStage(models.Model):
    _name = 'tech.stage'
    _rec_name = 'name'
    _order = "sequence"

    name = fields.Char(string='Stage Name')
    code = fields.Char(sring='Stage Code')
    machine_ids = fields.Char('Machines')
    description = fields.Char('Description')
    waste_percent = fields.Float('Waste Percent')
    sequence = fields.Many2one('tech.sequence', string='Sequence')
    tech_process_id = fields.Many2one('tech.process')


class TechProcess(models.Model):
    _name = 'tech.process'
    _rec_name = 'name'
    _order = "sequence"

    name = fields.Char(string='Process Name')
    code = fields.Char(string='Process Code')
    tech_stage_ids = fields.One2many('tech.stage',
                                     'tech_process_id',
                                     string='Technical Stages')
    description = fields.Char(string='Process Description')
    input_description = fields.Char(string='Input Description')
    input = fields.One2many('product.product',
                            'tech_process_id',
                            string="Input")
    output_description = fields.Char(string='Output Description')
    output = fields.Many2one('product.product',
                             string='Output')
    image = fields.Image(string='Image')
    sequence = fields.Many2one('tech.sequence', string='Sequence')
    ng_percent = fields.Float(string='NG Percent')
    bom_id = fields.Many2one('mrp.bom',
                             string='BOM')
    worker_group_ids = fields.One2many('worker.group', 'tech_process_id', string='Worker Group')


class Bom(models.Model):
    _inherit = ['mrp.bom']

    tech_process_ids = fields.One2many('tech.process', 'bom_id',
                                       string='Technical Process')
    time_process = fields.Float('Time Process')
    waste_percent = fields.Float(string='Waste Percent')
    ng_percent = fields.Float(string='NG Percent')
    created_by = fields.Many2one('res.users',
                                 string='Created By')
    worker_group_ids = fields.One2many('worker.group', 'bom_id', string='Worker Group')


