# -*- coding: utf-8 -*-

from odoo import models, fields, api

class TechSequence(models.Model):
    _name = 'tech.sequence'
    _rec_name = 'order'

    order = fields.Integer(string='Order')


class TechProcess(models.Model):
    _name = 'tech.process'
    _rec_name = 'name'

    name = fields.Char(string='Process Name')
    description = fields.Char(string='Process Description')
    input_description = fields.Char(string='Input Description')
    output_description = fields.Char(string='Output Description')
    image = fields.Image(string='Image')
    sequence = fields.Many2one('tech.sequence', string='Sequence')

class Bom(models.Model):
    _inherits = ['mrp.bom']

    tech_process_ids = fields.Many2one('tech.process')


