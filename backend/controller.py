from json import dumps as json
from odoo import http
from odoo.addons.web.controllers.main import serialize_exception
from . import tools
from . import routes

def authenticate(request, response):
    response.result = {'status': 'denied'}
    #if getattr(request, 'query'): request.params = tools.merge(request.params, request.query);
    params = tools.parse(request.params)
    if request.params.login:
       if 'encrypted' in params and params.encrypted == True:
          params.login, params.password = routes.decrypt(params.login), routes.decrypt(params.password)
       if 'database' not in params or not params.database:
          from odoo.service.db import list_dbs
          params.database = list_dbs()[0]
       uid = http.request.session.authenticate(params.database, params.login, params.password)
       if uid:
          user_id = http.request.env['res.users'].browse(uid)
          if user_id:
             #request.env.context.user = user_id
             response.result = {'status': 'success'}
             if True:
                response.result['login'], response.result['password'] = routes.encrypt(params.login), routes.encrypt(params.password)
                response.result['id'] = uid
                if 'client_js_time' not in params or not params.client_js_time or params.client_js_time != routes.client_js_time:
                   response.result['client_js'] = routes.client_js
                   response.result['client_js_time'] = routes.client_js_time
    return response.result

def iter_params(self):
    for key in dir(self):
        if key[0] != '_': yield key

class Api(http.Controller):

    @http.route('/api/login', type='http', auth='none', csrf=False)
    @serialize_exception
    def login(self, **kwargs):
        kwargs['__iter__'] = iter_params
        params = type('Params', tuple(), kwargs)()
        request = type('Request', tuple(), {'params': params})()
        response = type('Response', tuple(), {'result': {}})()
        authenticate(request, response)
        if response.result.get('status') != 'success': return http.request.make_response(json(response.result), [('Access-Control-Allow-Origin', '*')])
        return http.request.make_response(json(response.result), [('Access-Control-Allow-Origin', '*')])

    @http.route('/api/browse', type='http', auth='none', csrf=False)
    def browse(self, **kwargs):
        kwargs['__iter__'] = iter_params
        params = type('Params', tuple(), kwargs)()
        request = type('Request', tuple(), {'params': params})()
        response = type('Response', tuple(), {'result': {}})()
        authenticate(request, response)
        if response.result.get('status') != 'success': return http.request.make_response(json(response.result), [('Access-Control-Allow-Origin', '*')])
        setattr(request, 'env', http.request.env)
        routes.browse(request, response)
        return http.request.make_response(json(response.result), [('Access-Control-Allow-Origin', '*')])

    @http.route('/api/search', type='http', auth='none', csrf=False)
    @serialize_exception
    def search(self, **kwargs):
        kwargs['__iter__'] = iter_params
        params = type('Params', tuple(), kwargs)()
        request = type('Request', tuple(), {'params': params})()
        response = type('Response', tuple(), {'result': {}})()
        authenticate(request, response)
        if response.result.get('status') != 'success': return http.request.make_response(json(response.result), [('Access-Control-Allow-Origin', '*')])
        setattr(request, 'env', http.request.env)
        routes.search(request, response)
        return http.request.make_response(json(response.result), [('Access-Control-Allow-Origin', '*')])

    @http.route('/api/create', type='http', auth='none', csrf=False)
    @serialize_exception
    def create(self, **kwargs):
        kwargs['__iter__'] = iter_params
        params = type('Params', tuple(), kwargs)()
        request = type('Request', tuple(), {'params': params})()
        response = type('Response', tuple(), {'result': {}})()
        authenticate(request, response)
        if response.result.get('status') != 'success': return http.request.make_response(json(response.result), [('Access-Control-Allow-Origin', '*')])
        setattr(request, 'env', http.request.env)
        routes.create(request, response)
        return http.request.make_response(json(response.result), [('Access-Control-Allow-Origin', '*')])

    @http.route('/api/write', type='http', auth='none', csrf=False)
    @serialize_exception
    def write(self, **kwargs):
        kwargs['__iter__'] = iter_params
        params = type('Params', tuple(), kwargs)()
        request = type('Request', tuple(), {'params': params})()
        response = type('Response', tuple(), {'result': {}})()
        authenticate(request, response)
        if response.result.get('status') != 'success': return http.request.make_response(json(response.result), [('Access-Control-Allow-Origin', '*')])
        setattr(request, 'env', http.request.env)
        routes.write(request, response)
        return http.request.make_response(json(response.result), [('Access-Control-Allow-Origin', '*')])

    @http.route('/api/unlink', type='http', auth='none', csrf=False)
    @serialize_exception
    def unlink(self, **kwargs):
        kwargs['__iter__'] = iter_params
        params = type('Params', tuple(), kwargs)()
        request = type('Request', tuple(), {'params': params})()
        response = type('Response', tuple(), {'result': {}})()
        authenticate(request, response)
        if response.result.get('status') != 'success': return http.request.make_response(json(response.result), [('Access-Control-Allow-Origin', '*')])
        setattr(request, 'env', http.request.env)
        routes.unlink(request, response)
        return http.request.make_response(json(response.result), [('Access-Control-Allow-Origin', '*')])

    @http.route('/api/methods', type='http', auth='none', csrf=False)
    @serialize_exception
    def methods(self, **kwargs):
        kwargs['__iter__'] = iter_params
        params = type('Params', tuple(), kwargs)()
        request = type('Request', tuple(), {'params': params})()
        response = type('Response', tuple(), {'result': {}})()
        authenticate(request, response)
        if response.result.get('status') != 'success': return http.request.make_response(json(response.result), [('Access-Control-Allow-Origin', '*')])
        setattr(request, 'env', http.request.env)
        routes.methods(request, response)
        return http.request.make_response(json(response.result), [('Access-Control-Allow-Origin', '*')])

