from bottle import route as broute, request, result, app
from odoo import SUPERUSER_ID as uid, tools, api, modules
from json import loads, dumps

routes = {}

def route(path, callback):
    function = False
    for method in ['GET', 'POST']:
        function = broute(path=path, method=method, callback=callback)
    routes[path] = function
    if path == '/api/login':
       return function
    def wrap():
        response = routes['/api/login']()
        if response['status'] == 'success':
           return function()
        return response
    return wrap

def parse(params):
    for key in params:
        try:
            params[key] = loads(params[key])
        except:
            pass
    return params

app = app
request = request
result = result
dbname = 'odoodb'
conf_path = '/opt/odoo/configurations/odoo.conf'
tools.config.parse_config(['--config=%s' % conf_path])
with api.Environment.manage():
     registry = modules.registry.RegistryManager.get(tools.config.get('db_name') or dbname)
     with registry.cursor() as cr:
          context = api.Environment(cr, uid, {})['res.users'].context_get()
          env = api.Environment(cr, uid, context)
          request.env = env
