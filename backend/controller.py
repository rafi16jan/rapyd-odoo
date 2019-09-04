from json import dumps as json
from odoo import http
from odoo.addons.web.controllers.main import serialize_exception
from . import tools
from . import routes

def authenticate(request, response):
    response.result = {'status': 'denied'}
    if getattr(request, query): request.params = tools.merge(request.params, request.query);
    params = tools.parse(request.params)
    if request.params.login:
       if params.encrypted == True:
          params.login, params.password = routes.decrypt(params.login), routes.decrypt(params.password)
       if not params.database:
          from odoo.service.db import list_dbs:
          params.database = list_dbs()[0]
       uid = http.request.session.authenticate(params.database, params.login, params.password)
       if uid:
          user_id = request.env['res.users'].browse(uid)
          if user_id:
             #request.env.context.user = user_id
             response.result = {'status': 'success'}
             if params.authentication == True:
                response.result['login'], response.result['password'] = routes.encrypt(params.login), routes.encrypt(params.password)
                response.result['id'] = uid
                if not params.client_js_time or params.client_js_time != routes.client_js_time:
                   response.result['client_js'] = routes.client_js
                   response.result['client_js_time'] = routes.client_js_time
    return response.result  

class Api(http.Controller):

    @http.route('/api/login', type='http', auth='none', csrf=False)
    @serialize_exception
    def login(self, **kwargs):
        params = type('Params', (,), kwargs)()
        request = type('Request', (,), {'env': http.request.env, 'params': params})()
        response = type('Response', (,), {'result': {}})()
        authenticate(request, response)
        if response.result.get('status') != 'success': return http.request.make_response(json(response.result), [('Access-Control-Allow-Origin', '*')])
        return http.request.make_response(json(response.result), [('Access-Control-Allow-Origin', '*')])

    @http.route('/api/browse', type='http', auth='none', csrf=False)
    def browse(self, **kwargs):
        params = type('Params', (,), kwargs)()
        request = type('Request', (,), {'env': http.request.env, 'params': params})()
        response = type('Response', (,), {'result': {}})()
        authenticate(request, response)
        if response.result.get('status') != 'success': return http.request.make_response(json(response.result), [('Access-Control-Allow-Origin', '*')])
        routes.browse(request, response)
        return http.request.make_response(json(response.result), [('Access-Control-Allow-Origin', '*')])

    @http.route('/api/search', type='http', auth='none', csrf=False)
    @serialize_exception
    def search(self, **kwargs):
        params = type('Params', (,), kwargs)()
        request = type('Request', (,), {'env': http.request.env, 'params': params})()
        response = type('Response', (,), {'result': {}})()
        authenticate(request, response)
        if response.result.get('status') != 'success': return http.request.make_response(json(response.result), [('Access-Control-Allow-Origin', '*')])
        routes.search(request, response)
        return http.request.make_response(json(response.result), [('Access-Control-Allow-Origin', '*')])

    @http.route('/api/create', type='http', auth='none', csrf=False)
    @serialize_exception
    def create(self, **kwargs):
        params = type('Params', (,), kwargs)()
        request = type('Request', (,), {'env': http.request.env, 'params': params})()
        response = type('Response', (,), {'result': {}})()
        authenticate(request, response)
        if response.result.get('status') != 'success': return http.request.make_response(json(response.result), [('Access-Control-Allow-Origin', '*')])
        routes.create(request, response)
        return http.request.make_response(json(response.result), [('Access-Control-Allow-Origin', '*')])

    @http.route('/api/write', type='http', auth='none', csrf=False)
    @serialize_exception
    def write(self, **kwargs):
        params = type('Params', (,), kwargs)()
        request = type('Request', (,), {'env': http.request.env, 'params': params})()
        response = type('Response', (,), {'result': {}})()
        authenticate(request, response)
        if response.result.get('status') != 'success': return http.request.make_response(json(response.result), [('Access-Control-Allow-Origin', '*')])
        routes.write(request, response)
        return http.request.make_response(json(response.result), [('Access-Control-Allow-Origin', '*')])

    @http.route('/api/unlink', type='http', auth='none', csrf=False)
    @serialize_exception
    def unlink(self, **kwargs):
        params = type('Params', (,), kwargs)()
        request = type('Request', (,), {'env': http.request.env, 'params': params})()
        response = type('Response', (,), {'result': {}})()
        authenticate(request, response)
        if response.result.get('status') != 'success': return http.request.make_response(json(response.result), [('Access-Control-Allow-Origin', '*')])
        routes.unlink(request, response)
        return http.request.make_response(json(response.result), [('Access-Control-Allow-Origin', '*')])

    @http.route('/api/methods', type='http', auth='none', csrf=False)
    @serialize_exception
    def methods(self, **kwargs):
        params = type('Params', (,), kwargs)()
        request = type('Request', (,), {'env': http.request.env, 'params': params})()
        response = type('Response', (,), {'result': {}})()
        authenticate(request, response)
        if response.result.get('status') != 'success': return http.request.make_response(json(response.result), [('Access-Control-Allow-Origin', '*')])
        routes.methods(request, response)
        return http.request.make_response(json(response.result), [('Access-Control-Allow-Origin', '*')])

