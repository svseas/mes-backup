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


class ProductProducts(models.Model):
    _inherit = 'product.product'

    tech_process_id = fields.Many2one('tech.process', string='Tech Process')
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

    name = fields.Char(string='Process Name')
    code = fields.Char(string='Process Code')
    description = fields.Char(string='Process Description')
    input_description = fields.Html(string='Input Description')
    input = fields.One2many('product.product',
                            'tech_process_id',
                            string="Input")
    output_description = fields.Html(string='Output Description')
    output = fields.Many2one('product.product',
                             string='Output')
    sfg = fields.Boolean(string='SFG', default=False)
    use_material = fields.Boolean(string='Material Use', default=True)
    use_machine = fields.Boolean(string='Machine Use', default=True)
    use_man = fields.Boolean(string='Worker Use', default=True)
    image = fields.Image(string='Image')
    documents = fields.Binary(string='Document')
    document_name = fields.Char(string="File Name")
    sequence = fields.Many2one('tech.sequence', string='Sequence')
    consumption_percent = fields.Float(string='% Consume')
    ng_percent = fields.Float(string='% NG')
    worker_group_ids = fields.Many2many('worker.group', string='Worker Group')
    bom_ids = fields.Many2many('mrp.bom', string='BOM')

    parent_process = fields.Many2one('tech.process', string='Parent Process')
    child_process_ids = fields.One2many('tech.process',
                                        'parent_process',
                                        string='Child Process', )


class Bom(models.Model):
    _inherit = ['mrp.bom']

    tech_process_ids = fields.Many2many('tech.process',
                                        string='Technical Process')
    time_process = fields.Float('Time Process*',
                                required=True,
                                default=0)
    consumption = fields.Float(string='Consumption Rate')
    waste_percent = fields.Float(string='Waste Percent*')
    ng_percent = fields.Float(string='NG Percent*',
                              required=True,
                              default=0)
    created_by = fields.Many2one('res.users',
                                 string='Created By*',
                                 required=True)
    worker_group_ids = fields.One2many('worker.group', 'bom_id', string='Worker Group')
    bom_uom = fields.Char(string='UOM', help="Unit of measurement")
