from odoo import models, fields, api


class MaterialProcurement(models.Model):
    """Material Procurement"""
    _name = 'material.procurement'
    _rec_name = 'code'

    code = fields.Char(string='Code', required=True)
    client = fields.Many2one('res.partner', string='Client', required=True)
    manufacturing_order = fields.Many2one('mes.manufacturing.order', string='Manufacturing Order', required=True)
