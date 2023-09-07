from odoo import models, fields, api


class DataTable(models.Model):
    _inherit = ['tech.process']
    _description = 'Data Table'

    @api.model
    def get_table_data(self):
        data = self.env['tech.process'].search([])
        return data.read()


