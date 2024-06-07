# -*- coding: utf-8 -*-
# from odoo import http


# class AppNaming(http.Controller):
#     @http.route('/app_naming/app_naming', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/app_naming/app_naming/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('app_naming.listing', {
#             'root': '/app_naming/app_naming',
#             'objects': http.request.env['app_naming.app_naming'].search([]),
#         })

#     @http.route('/app_naming/app_naming/objects/<model("app_naming.app_naming"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('app_naming.object', {
#             'object': obj
#         })

