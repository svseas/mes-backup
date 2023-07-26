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


class MaterialLine(models.Model):
    _name = 'material.line'
    _description = 'material line for tech process'
    _rec_name = 'material'

    material = fields.Many2one('material.material', string='Material')
    mat_qty = fields.Float(string='Quantity')
    mat_uom = fields.Char(string='UOM')
    mat_waste = fields.Float(string='% Waste')
    tech_process_id = fields.Many2one('tech.process', readonly=True)


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
    input = fields.One2many('material.line', 'tech_process_id',
                            string="Input")
    input_description = fields.Html(string='Input Description')
    # input_char = fields.Char(string='Test Input', compute='_propagate_material_to_parent')
    machine = fields.Many2one('equipment.template', string='Machine')
    machine_hours = fields.Float('Machine Hours')
    worker_group_ids = fields.Many2one('worker.group', string='Worker Type')
    worker_hours = fields.Float('Worker Hours')
    waste_percent = fields.Float(string='% Waste')
    output = fields.Many2one('material.line',
                             string='Output')
    output_description = fields.Html(string='Output Description')
    image = fields.Image(string='Image')
    documents = fields.Binary(string='Document')
    document_name = fields.Char(string="File Name")
    ng_percent = fields.Float(string='% NG')
    child_process_inputs = fields.Many2many('material.line', compute='_compute_child_inputs', string='Child Inputs')

    @api.depends('child_process_ids', 'child_process_ids.input')
    def _compute_child_inputs(self):
        def get_child_inputs(process, is_root=True):
            inputs = process.env['material.line']
            if not is_root:
                inputs = process.mapped('input')
            for child in process.child_process_ids:
                inputs |= get_child_inputs(child, is_root=False)
            return inputs

        for record in self:
            all_inputs = get_child_inputs(record)
            record.child_process_inputs = [(6, 0, all_inputs.ids)]

    # @api.onchange('child_process_ids')
    # def _propagate_material_to_parent(self):
    #     for record in self:
    #         if record.child_process_ids:
    #             parent_materials = record.input
    #             child_materials = record.child_process_ids.input
    #             # add child materials to parent that are not already there
    #             materials_to_add = child_materials - parent_materials
    #             if materials_to_add:
    #                 record.input_char = materials_to_add
    #             record.input_char = 'NONE'

    # @api.model
    # def create(self, vals):
    #     record = super(TechProcess, self).create(vals)
    #     record.with_context(skip_recursion=True)._add_child_inputs_to_parent()
    #     return record
    #
    # def write(self, vals):
    #     res = super(TechProcess, self).write(vals)
    #     # Here, we add a context flag to avoid infinite recursion
    #     if not self.env.context.get('skip_recursion'):
    #         self.with_context(skip_recursion=True)._add_child_inputs_to_parent()
    #     return res
    #
    # def _add_child_inputs_to_parent(self):
    #     for record in self:
    #         if record.child_process_ids:
    #             child_inputs = record.mapped('child_process_ids.input')
    #             parent_inputs = record.input
    #             # Union of child and parent inputs
    #             all_inputs = parent_inputs | child_inputs
    #             # Update the parent process's input field without triggering recursion
    #             record.with_context(skip_recursion=True).input = [(6, 0, all_inputs.ids)]


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
