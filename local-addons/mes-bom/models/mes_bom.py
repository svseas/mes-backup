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

class TechProcess(models.Model):
    _name = 'tech.process'
    _rec_name = 'name'

    name = fields.Char(string='Process Name')
    tech_stage_ids = fields.Many2one(string='Technical Stage')
    description = fields.Char(string='Process Description')
    input_description = fields.Char(string='Input Description')
    output_description = fields.Char(string='Output Description')
    image = fields.Image(string='Image')
    sequence = fields.Many2one('tech.sequence', string='Sequence')
    ng_percent = fields.Float(string='NG Percent')


class Bom(models.Model):
    _inherits = ['mrp.bom']

    tech_process_ids = fields.Many2one('tech.process', 'Technical Process')
    time_process = fields.Float('Time Process')
    tech_process_ids = fields.Many2one('tech.process')

"""Tran Viet check feature"""