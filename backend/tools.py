import json
from odoo.tools import *

def merge(*args):
    if not args:
       return
    target, merges = args[0], args[1:]
    for merge in merges:
        target.update(merge)
    return target

def parse(params):
    for key in params:
        try:
            setattr(params, key, json.loads(getattr(params, key))
        except:
            pass
        try:
            params[key] = json.loads(params[key])
        except:
            pass
    return params

def each(value):
    if type(value) == list: return value
    return [value]
