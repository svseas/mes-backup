# -*- coding: utf-8 -*-
from odoo import models, fields, api


class EquipmentTemplate(models.Model):
    """EQUIPMENT USED IN TECH PROCESS"""
    _name = 'equipment.template'
    _description = 'Equipment Template'
    _rec_name = 'name'

    name = fields.Char(string='Name')
    code = fields.Char(string='Code')
    position = fields.Char(string='Position')


class EquipmentUsage(models.Model):
    """EQUIPMENT LINE"""
    _name = 'equipment.usage'
    _description = 'Equipment Usage in Tech Process'
    _rec_name = 'machine'

    machine = fields.Many2one('equipment.template', string='Machine')
    machine_hours = fields.Float('Machine Hours')
    tech_process_id = fields.Many2one('tech.process', string='Tech Process')
