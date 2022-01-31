# -*- coding: utf-8 -*-
from odoo import http

# class IqmindDashboard(http.Controller):
#     @http.route('/iqmind_dashboard/iqmind_dashboard/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/iqmind_dashboard/iqmind_dashboard/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('iqmind_dashboard.listing', {
#             'root': '/iqmind_dashboard/iqmind_dashboard',
#             'objects': http.request.env['iqmind_dashboard.iqmind_dashboard'].search([]),
#         })

#     @http.route('/iqmind_dashboard/iqmind_dashboard/objects/<model("iqmind_dashboard.iqmind_dashboard"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('iqmind_dashboard.object', {
#             'object': obj
#         })