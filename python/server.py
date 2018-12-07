import tools
import http
import json
import os
request = http.request
result = http.result

client_js = os.environ['rapyd_client_js']
del os.environ['rapyd_client_js']
configuration = tools.merge(configuration, {key: True if value in ['True', 'true'] else False if value in ['False', 'false'] else value for key, value in os.environ.items()})

#admin_password = configuration.admin_password

#client_js = require('child_process').execSync(require('process').execPath + ' ./node_modules/.bin/rapydscript -p modules/ client.pyj', {'env': require('process').env}).toString()
client_js = client_js.replace('{"home_view": window.localStorage.rapyd_home_view || "res.message.chat"}', json.dumps(configuration))
client_js_time = tools.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

#crypto = require('crypto')
from cryptography.fernet import Fernet

def encrypt(string):
    key = 'JtSYGIV4XnR0qqXJrZzaBJxcx3xeuitIZk8werZmuJw=' or configuration.crypto_key
    fernet = Fernet(key)
    return fernet.encrypt(string)

def decrypt(string):
    key = 'JtSYGIV4XnR0qqXJrZzaBJxcx3xeuitIZk8werZmuJw=' or configuration.crypto_key
    fernet = Fernet(key)
    return fernet.decrypt(string)

@http.route('/api/login')
def login():
    request.env = env
    result.response = {'status': 'denied'}
    request.params = tools.merge(request.params, request.query);
    params = http.parse(request.params)
    if request.params.login:
       if params.encrypted == True:
          params.login, params.password = decrypt(params.login), decrypt(params.password)
       uid = request.env['res.users']._login(http.dbname, params.login, params.password)
       if uid:
          user_id = request.env['res.users'].browse(uid)
          if user_id:
             #request.env.context.user = user_id
             result.response = {'status': 'success'}
             if params.authentication = True:
                result.response.login, result.response.password = encrypt(params.login), encrypt(params.password)
                result.response.id = uid
                if not params.client_js_time or params.client_js_time != client_js_time:
                   result.response.client_js = client_js
                   result.response.client_js_time = client_js_time
    return result.response

@http.route('/api/browse')
def browse():
    params = request.params
    if request.params:
       record = request.env[params.model].browse(params.ids)
       values = record.read(load=False)
       if len(values) == 1:
          values = values[0]
       elif len(values) < 1:
          values = {}
       result.response = {'status': 'success', 'values': values}
    return result.response

@http.route('/api/search'
def search():
    params = request.params
    if request.params:
       record = request.env[params.model].search(params.args, **params.options)
       values = record.read(load=False)
       if len(values) == 1:
          values = values[0]
       elif len(values) < 1:
          values = {}
       result.response = {'status': 'success', 'values': values}
    return result.response

@http.route('/api/create')
def search():
    params = request.params
    if request.params:
       record = request.env[params.model].create(params.values)
       values = record.read(load=False)
       if len(values) == 1:
          values = values[0]
       elif len(values) < 1:
          values = {}
       result.response = {'status': 'success', 'values': values}
    return result.response

@http.route('/api/write')
def write():
    params = request.params
    if request.params:
       record = request.env[params.model].browse(params.ids).write(params.values)
       values = record.read(load=False)
       if len(values) == 1:
          values = values[0]
       elif len(values) < 1:
          values = {}
       result.response = {'status': 'success', 'values': values}
    return result.response

@http.route('/api/unlink')
def unlink():
    params = request.params
    if request.params:
       record = request.env[params.model].browse(params.ids).unlink()
       result.response = {'status': 'success'}
    return result.response

@http.route('/api/methods')
def methods():
    params = request.params
    if request.params:
       args = params.args if 'args' in params else []
       record = getattr(request.env[params.model].browse(params.ids), params.method)(*args)
       values = record.read(load=False)
       if len(values) == 1:
          values = values[0]
       elif len(values) < 1:
          values = {}
       result.response = {'status': 'success', 'values': values}
    return result.response

app = http.app
if __name__ == '__main__':
   app.run()
