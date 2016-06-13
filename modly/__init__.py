
import imp, sys, string, random

import getters

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def get_module(module_string, module_name = None):
    new_module = imp.new_module(module_name if module_name else id_generator())
    exec module_string in new_module.__dict__
    return new_module
