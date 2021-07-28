# -*- coding: utf-8 -*-
from odoo import http

# class BudgetApplication(http.Controller):
#     @http.route('/budget_application/budget_application/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/budget_application/budget_application/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('budget_application.listing', {
#             'root': '/budget_application/budget_application',
#             'objects': http.request.env['budget_application.budget_application'].search([]),
#         })

#     @http.route('/budget_application/budget_application/objects/<model("budget_application.budget_application"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('budget_application.object', {
#             'object': obj
#         })