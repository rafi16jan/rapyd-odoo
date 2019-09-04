from . import tools
import subprocess
import json

Fernet = None
try:
    from cryptography.fernet import Fernet
except:
    pass

client_js = subprocess.check_output(['node', __file__.replace('routes.pyc', 'odoo.js').replace('routes.py', 'odoo.js')])
configuration = json.loads(open(__file__.replace('routes.pyc', 'config.json').replace('routes.py', 'config.json'), 'r').read())
client_js_time = tools.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def encrypt(string):
    if not Fernet: return string
    key = 'JtSYGIV4XnR0qqXJrZzaBJxcx3xeuitIZk8werZmuJw=' or configuration.crypto_key
    fernet = Fernet(key)
    return fernet.encrypt(bytes(string))

def decrypt(string):
    if not Fernet: return string
    key = 'JtSYGIV4XnR0qqXJrZzaBJxcx3xeuitIZk8werZmuJw=' or configuration.crypto_key
    fernet = Fernet(key)
    return fernet.decrypt(bytes(string))

def login(request, response):
    response.result = {'status': 'denied'}
    if getattr(request, query): request.params = tools.merge(request.params, request.query);
    params = tools.parse(request.params)
    if request.params.login:
       if params.encrypted == True:
          params.login, params.password = decrypt(params.login), decrypt(params.password)
       uid = request.env['res.users']._login(http.dbname, params.login, params.password)
       if uid:
          user_id = request.env['res.users'].browse(uid)
          if user_id:
             #request.env.context.user = user_id
             response.result = {'status': 'success'}
             if params.authentication == True:
                response.result['login'], response.result['password'] = encrypt(params.login), encrypt(params.password)
                response.result['id'] = uid
                if not params.client_js_time or params.client_js_time != client_js_time:
                   response.result['client_js'] = client_js
                   response.result['client_js_time'] = client_js_time
    return response.result

def browse(request, response):
    params = request.params
    if request.params:
       record = request.env[params.model].browse(params.ids)
       values = record.read(load=False)
       if len(values) == 1:
          values = values[0]
       elif len(values) < 1:
          values = {}
       response.result = {'status': 'success', 'values': values}
    return response.result

def search(request, response):
    params = request.params
    if request.params:
       record = request.env[params.model].search(params.args, **params.options)
       values = record.read(load=False)
       if len(values) == 1:
          values = values[0]
       elif len(values) < 1:
          values = {}
       response.result = {'status': 'success', 'values': values}
    return response.result

def create():
    params = request.params
    if request.params:
       values = []
       for value in tools.each(params.values):
           record = request.env[params.model].create(value)
           values += record.read(load=False)
       if len(values) == 1:
          values = values[0]
       elif len(values) < 1:
          values = {}
       response.result = {'status': 'success', 'values': values}
    return response.result

def write(request, response):
    params = request.params
    if request.params:
       values = []
       if type(params.values) == list and type(params.ids) == list:
          if len(params.value) == len(params.ids):
             for id, value in zip(params.ids, params.values):
                 record = request.env[params.model].browse(id).write(value)
                 values += record.read(load=False)
          else:
             response.result = {'status': 'error', 'error': 'Invalid Write Operation'}
             return response.result
       for value in tools.each(params.values):
           record = request.env[params.model].browse(params.ids).write(value)
           values += record.read(load=False)
       if len(values) == 1:
          values = values[0]
       elif len(values) < 1:
          values = {}
       response.result = {'status': 'success', 'values': values}
    return response.result

def unlink(request, response):
    params = request.params
    if request.params:
       record = request.env[params.model].browse(params.ids).unlink()
       response.result = {'status': 'success'}
    return response.result

def methods(request, response):
    params = request.params
    if request.params:
       args = params.args if 'args' in params else []
       record = getattr(request.env[params.model].browse(params.ids), params.method)(*args)
       values = record.read(load=False)
       if len(values) == 1:
          values = values[0]
       elif len(values) < 1:
          values = {}
       response.result = {'status': 'success', 'values': values}
    return response.result
