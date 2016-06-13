
import os, base64, imp, sys, string, random

from github import Github

here = os.path.dirname(os.path.abspath(__file__))
g = Github(open(os.path.join(here,'..','.github_token'), 'r').read())

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def get_github_string(user, repo, fname):
    return base64.b64decode(
        g.get_repo('{}/{}'.format(user, repo))\
            .get_contents('test/tmod.py').content
    )

def get_github_module(user, repo, fname, module_name=None):
    return get_module(
        get_github_string(user, repo, fname),
        module_name
    )

def get_module(module_string, module_name=None):
    new_module = imp.new_module(module_name if module_name else id_generator())
    exec module_string in new_module.__dict__
    return new_module
