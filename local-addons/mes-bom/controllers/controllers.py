# -*- coding: utf-8 -*-
# from odoo import http


# class Mes-bom(http.Controller):
#     @http.route('/mes-bom/mes-bom', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mes-bom/mes-bom/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('mes-bom.listing', {
#             'root': '/mes-bom/mes-bom',
#             'objects': http.request.env['mes-bom.mes-bom'].search([]),
#         })

#     @http.route('/mes-bom/mes-bom/objects/<model("mes-bom.mes-bom"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mes-bom.object', {
#             'object': obj
#         })
