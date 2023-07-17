# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TechSequence(models.Model):
    """Technological Sequence to be added"""
    _name = 'tech.sequence'
    _rec_name = 'order'

    order = fields.Integer(string='Order')


class TechStage(models.Model):
    _name = 'tech.stage'
    _rec_name = 'name'

    name = fields.Char('Stage Name')
    machine_ids = fields.Char('Machines')
    description = fields.Char('Description')
    waste_percent = fields.Float('Waste Percent')
    sequence = fields.Many2one('tech.sequence', string='Sequence')
    tech_process_id = fields.Many2one('tech.process')


class TechProcess(models.Model):
    _name = 'tech.process'
    _rec_name = 'name'

    name = fields.Char(string='Process Name')
    tech_stage_ids = fields.One2many('tech.stage',
                                     'tech_process_id',
                                     string='Technical Stages')
    description = fields.Char(string='Process Description')
    input_description = fields.Char(string='Input Description')
    input = fields.Many2one('product.product',
                            string="Input")
    output_description = fields.Char(string='Output Description')
    output = fields.Many2one('product.product',
                             string='Output')
    image = fields.Image(string='Image')
    sequence = fields.Many2one('tech.sequence', string='Sequence')
    ng_percent = fields.Float(string='NG Percent')
    bom_id = fields.Many2one('mrp.bom')


class Bom(models.Model):
    _inherit = ['mrp.bom']

    tech_process_ids = fields.One2many('tech.process', 'bom_id',
                                       string='Technical Process')
    time_process = fields.Float('Time Process')
    waste_percent = fields.Float(string='Waste Percent')
    ng_percent = fields.Float(string='NG Percent')
    created_by = fields.Many2one('res.users',
                                 string='Created By')

