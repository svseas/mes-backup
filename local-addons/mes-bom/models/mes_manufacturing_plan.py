from odoo import fields, api, models, exceptions
from datetime import datetime


class ProcurementPlan(models.Model):
    _name = 'mes.procurement.plan'
    _description = 'Procurement Plan'
    _rec_name = 'code'

    code = fields.Char(string='Code', required=True, default='New')
    delivery_schedule_id = fields.Many2one('delivery.schedule', string='Delivery Schedule', required=True,
                                           ondelete='cascade')
    delivery_date = fields.Date(related='delivery_schedule_id.delivery_date', string='Delivery Date')
    bom_id = fields.Many2one('mrp.bom', string='BOM', related='delivery_schedule_id.bom')
    quantity = fields.Float(related='delivery_schedule_id.quantity', string='Quantity')
    material_ids = fields.Many2many('material.line', string='Materials', related='bom_id.combined_inputs')
    calculated_material_ids = fields.One2many('mes.procurement.plan.material', 'procurement_plan_id',
                                              string='Calculated Materials', compute='_compute_material_quantities',
                                              store=True)

    @api.depends('material_ids', 'quantity')
    def _compute_material_quantities(self):
        for plan in self:
            # Clear existing calculated materials
            plan.calculated_material_ids.unlink()

            # Calculate new material quantities
            new_materials = []
            for material_line in plan.material_ids:
                calculated_quantity = plan.quantity * material_line.mat_qty * (1 + material_line.mat_waste)
                new_materials.append((0, 0, {
                    'material_id': material_line.material.id, 
                    'mat_qty': material_line.mat_qty,
                    'mat_uom': material_line.mat_uom,
                    'mat_waste': material_line.mat_waste,
                    'calculated_quantity': calculated_quantity,
                }))
            plan.calculated_material_ids = new_materials


class ProcurementPlanMaterial(models.Model):
    _name = 'mes.procurement.plan.material'
    _description = 'Model for Calculated Material Quantities'

    procurement_plan_id = fields.Many2one('mes.procurement.plan', string='Procurement Plan', ondelete='cascade')
    material_id = fields.Many2one('material.material', string='Material')
    mat_qty = fields.Float(string='Quantity')
    mat_uom = fields.Char(string='UOM')
    mat_waste = fields.Float(string='% Waste')
    calculated_quantity = fields.Float(string='Calculated Quantity')
    

