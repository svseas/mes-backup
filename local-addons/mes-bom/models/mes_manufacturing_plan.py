from odoo import fields, api, models, exceptions
from datetime import datetime


class ProcurementPlan(models.Model):
    _name = 'mes.procurement.plan'
    _description = 'Procurement Plan'
    _rec_name = 'code'
    
    code = fields.Char(string='Code', required=True, copy=False, default='New Code')
    manufacturing_order_id = fields.Many2one('mes.manufacturing.order', string='Manufacturing Order', required=True)
