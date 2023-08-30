from odoo import models, fields, api


class TableTest(models.Model):
    _name = "table.test"
    _description = 'Table Test'

    name = fields.Char(string='Name*')


