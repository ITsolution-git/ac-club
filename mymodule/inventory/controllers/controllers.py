# -*- coding: utf-8 -*-
from odoo import http

# class Inventory(http.Controller):
#     @http.route('/inventory/inventory/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inventory/inventory/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('inventory.listing', {
#             'root': '/inventory/inventory',
#             'objects': http.request.env['inventory.inventory'].search([]),
#         })

#     @http.route('/inventory/inventory/objects/<model("inventory.inventory"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inventory.object', {
#             'object': obj
#         })