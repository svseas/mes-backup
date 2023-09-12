from odoo import models, fields


class InheritProduct(models.Model):
    _inherit = ['mrp.bom']
    _description = 'Table Test'

    name = fields.Char(string='Name*')

    def button_table_view(self):
        action = self.env.ref('mes-bom.action_data_table_js').read()[0]
        return action
