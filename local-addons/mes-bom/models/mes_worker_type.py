from odoo import models, fields, api


# WORKER TYPE USED IN TECH PROCESS

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


class WorkerTypeUsage(models.Model):
    _name = 'worker.type.usage'
    _rec_name = 'worker_group_ids'

    worker_group_ids = fields.Many2one('worker.group', string='Worker Type')
    worker_hours = fields.Float('Worker Hours')
    tech_process_id = fields.Many2one('tech.process', string='Tech Process')
