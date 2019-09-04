from . import tools
from . import http
from . import routes
import json
request = http.request
response = http.response

#configuration = {key: True if value in ['True', 'true'] else False if value in ['False', 'false'] else value for key, value in os.environ.items()}

#admin_password = configuration.admin_password

@http.route('/api/login')
def login():
    return routes.login(request, response)

@http.route('/api/browse')
def browse():
    return routes.browse(request, response)

@http.route('/api/search')
def search():
    return routes.search(request, response)

@http.route('/api/create')
def create():
    return routes.create(request, response)


@http.route('/api/write')
def write():
    return routes.write(request, response)

@http.route('/api/unlink')
def unlink():
    return routes.unlink(request, response)

@http.route('/api/methods')
def methods():
    return routes.methods(request, response)

app = http.app
if __name__ == '__main__':
   from bottle import run
   run(host='0.0.0.0')
