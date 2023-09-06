from odoo import models, fields, api, exceptions


class InheritProduct(models.Model):
    _inherit = ['material.material']
    _description = 'Table Test'

    name = fields.Char(string='Name*')

    def button_table_view(self):
        action = self.env.ref('mes-bom.action_data_table_js').read()[0]
        return action
