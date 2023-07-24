# -*- coding: utf-8 -*-

from odoo import models, fields, api


# TO DO
# REFACTOR WORKER INTO DIFFERENT ADD-ON: MES-WORKER
class MrpWorkerGroup(models.Model):
    """Worker Group for BOM and other modules in MRP"""
    _name = 'worker.group'
    _rec_name = 'name'

    name = fields.Char(string='Group Name')
    code = fields.Char(string='Group Code')
    expertise_level = fields.Selection(selection=[('type_one', '2/7'),
                                                  ('type_two', '3/7'),
                                                  ('type_three', '4/7'),
                                                  ('type_four', '5/7'),
                                                  ('type_five', '6/7'),
                                                  ('type_six', '7/7')])
    worker_ids = fields.Many2many('res.users',
                                  string="Worker List")
    bom_id = fields.Many2one('mrp.bom', string='BOM')
    tech_process_id = fields.Many2many('tech.process', string='Technical Process')


class EquipmentTemplate(models.Model):
    _name = 'equipment.template'
    _description = 'Equipment Template'
    _rec_name = 'name'

    name = fields.Char(string='Name')
    code = fields.Char(string='Code')
    position = fields.Char(string='Position')


class MaterialMaterials(models.Model):
    _name = 'material.material'
    _description = 'Materials used for BOM'
    _rec_name = 'name'

    name = fields.Char(string='Name*')
    code = fields.Char(sring='Code*')
    description = fields.Html(string='Description')
    electronic_material = fields.Boolean(string='Electronic Material', default=False)
    designator = fields.Char(string='Designator', help='Electronic Material')
    footprint = fields.Char(string='Footprint')
    lib_ref = fields.Char(string='Lib Ref')
    manufacturer_name = fields.Char(string='Manufacturer Name')
    supplier_name = fields.Char(string='Supplier Name')
    supplier_code = fields.Char(string='Supplier Code')


class ProductProducts(models.Model):
    _inherit = 'product.product'

    manufacturing_type = fields.Selection(selection=[('sfg', 'SFG'), ('material', 'Material')],
                                          default='sfg')

class TechSequence(models.Model):
    """Technological Sequence to be added"""
    _name = 'tech.sequence'
    _rec_name = 'order'

    order = fields.Integer(string='Order')


class TechProcess(models.Model):
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
    input = fields.Many2many('material.material',
                             string="Input")
    input_description = fields.Html(string='Input Description')
    machine = fields.Many2one('equipment.template', string='Machine')
    machine_hours = fields.Float('Machine Hours')
    worker_group_ids = fields.Many2one('worker.group', string='Worker Type')
    worker_hours = fields.Float('Worker Hours')
    consumption_percent = fields.Float(string='% Consume')
    output = fields.Many2one('material.material',
                             string='Output')
    output_description = fields.Html(string='Output Description')
    image = fields.Image(string='Image')
    documents = fields.Binary(string='Document')
    document_name = fields.Char(string="File Name")
    ng_percent = fields.Float(string='% NG')



class Bom(models.Model):
    _inherit = ['mrp.bom']

    tech_process_ids = fields.Many2many('tech.process',
                                        string='Technical Process')
    time_process = fields.Float('Time Process*',
                                required=True,
                                default=0)
    waste_percent = fields.Float(string='Waste Percent*')
    ng_percent = fields.Float(string='NG Percent*',
                              required=True,
                              default=0)
    created_by = fields.Many2one('res.users',
                                 string='Created By*',
                                 required=True)
    # worker_group_ids = fields.One2many('worker.group', 'bom_id', string='Worker Group')
    bom_uom = fields.Char(string='UOM', help="Unit of measurement")
