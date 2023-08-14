from odoo import models, fields, api


class ManufacturingOrder(models.Model):
    """Manufacturing Order"""
    _name = 'mes.manufacturing.order'
    _rec_name = 'name'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True)
    product = fields.Many2one('product.product', string='Product', required=True)
    bom = fields.Many2one('mrp.bom', string='BOM', required=True)
    quantity = fields.Float(string='Quantity*', required=True, default=1.0)
    uom = fields.Char(string='UOM', required=True)
    created_by = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user)
    approved_by = fields.Many2one('res.users', string='Approved By', default=lambda self: self.env.user)
    date_start = fields.Date(string='Date Start', required=True)
    date_end = fields.Date(string='Date End', required=True)
    contract_id = fields.Char(string='Contract ID')
    customer_id = fields.Many2one('res.partner', string='Customer')
    document = fields.Binary(string='Document')
    # bom_tech_process_ids = fields.Many2many(related='bom.tech_process_ids', string='BOM Tech Processes')
    #
    # combined_inputs = fields.Many2many(related='bom.combined_inputs', string='Combined Inputs')




