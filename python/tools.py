from odoo.tools import *
def merge(*args):
    if not args:
       return
    target, merges = args[0], args[1:]
    for merge in merges:
        target.update(merge)
    return target
