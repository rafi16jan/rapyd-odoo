from bottle import route as broute, LocalRequest, LocalResponse, app
from odoo import SUPERUSER_ID as uid, tools, api, modules
from json import loads, dumps
from os import environ

routes = {}

def route(path):
    def wrap(callback):
        function = False
        for method in ['GET', 'POST']:
           function = broute(path=path, method=method, callback=callback)
        routes[path] = function
        if path == '/api/login':
           return function
        def wrap_again(*args, **kwargs):
            result = routes['/api/login'](*args, **kwargs)
            if hasattr(response, 'result') and response.result['status'] == 'success':
               return function(*args, **kwargs)
            return result
        return wrap_again
    return wrap

def parse(params):
    for key in params:
        try:
            params[key] = loads(params[key])
        except:
            pass
    return params

app = app
dbname = environ.get('server_db', 'odoo_db')
conf_path = '/opt/odoo/configurations/odoo.conf'
tools.config.parse_config(['--config=%s' % conf_path])
_local = api.Local()
_local.environments = api.Environments()
api.Environment._local = _local
registry = modules.registry.RegistryManager.get(tools.config.get('db_name') or dbname)
cr = registry.cursor()
context = api.Environment(cr, uid, {})['res.users'].context_get()
env = api.Environment(cr, uid, context)
request = type('Request', (LocalRequest,), {'env': env})()
response = type('Response', (LocalResponse,), {'result': {}})()
