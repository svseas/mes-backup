# -*- coding: utf-8 -*-

from odoo import models, fields, api

"""MATERIALS USED IN TECH PROCESS"""


class MaterialMaterials(models.Model):
    _name = 'material.material'
    _description = 'Materials used for BOM'
    _rec_name = 'name'

    name = fields.Char(string='Name*')
    code = fields.Char(string='Code*')
    description = fields.Html(string='Description')
    electronic_material = fields.Boolean(string='Electronic Material', default=False)
    designator = fields.Char(string='Designator', help='Electronic Material')
    footprint = fields.Char(string='Footprint')
    lib_ref = fields.Char(string='Lib Ref')
    manufacturer_name = fields.Char(string='Manufacturer Name')
    supplier_name = fields.Char(string='Supplier Name')
    supplier_code = fields.Char(string='Supplier Code')


class MaterialLine(models.Model):
    _name = 'material.line'
    _description = 'material line for tech process'
    _rec_name = 'material'

    material = fields.Many2one('material.material', string='Material')
    mat_qty = fields.Float(string='Quantity')
    mat_uom = fields.Char(string='UOM')
    mat_waste = fields.Float(string='% Waste')
    tech_process_id = fields.Many2one('tech.process', readonly=True)

    # Related fields to get material info
    name = fields.Char(related='material.name', readonly=True, string='Name')
    code = fields.Char(related='material.code', readonly=True, string='Code')
    description = fields.Html(related='material.description', readonly=True, string='Description')
    electronic_material = fields.Boolean(related='material.electronic_material', readonly=True,
                                         string='Electronic Material')
    designator = fields.Char(related='material.designator', readonly=True, string='Designator')
    footprint = fields.Char(related='material.footprint', readonly=True, string='Footprint')
    lib_ref = fields.Char(related='material.lib_ref', readonly=True, string='Lib Ref')
    manufacturer_name = fields.Char(related='material.manufacturer_name', readonly=True, string='Manufacturer Name')
    supplier_name = fields.Char(related='material.supplier_name', readonly=True, string='Supplier Name')
    supplier_code = fields.Char(related='material.supplier_code', readonly=True, string='Supplier Code')


class OutputLine(models.Model):
    _name = 'output.line'
    _rec_name = 'output'

    output = fields.Many2one('material.material', string='Output')
    output_description = fields.Html('Output Description')
    tech_process_id = fields.Many2one('tech.process')
