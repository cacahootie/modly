
import os, base64, imp, sys, string, random, json

import github
from github import Github

here = os.path.dirname(os.path.abspath(__file__))
g = Github(open(os.path.join(here,'..','.github_token'), 'r').read())

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def get_github_string(user, repo, fname, branch=None):
    return base64.b64decode(
        g.get_repo('{}/{}'.format(user, repo))\
            .get_contents(fname, ref=branch or 'master').content
    )

def get_github_json(*args, **kwargs):
    try:
        return json.loads(get_github_string(*args, **kwargs))
    except github.GithubException:
        return None

def get_github_module(user, repo, fname, module_name=None, branch=None):
    return get_module(
        get_github_string(user, repo, fname, branch),
        module_name if branch is None else "{}_{}".format(module_name, branch)
    )

def get_module(module_string, module_name=None):
    new_module = imp.new_module(module_name if module_name else id_generator())
    bc = compile(module_string, '<string>', 'exec')
    exec bc in new_module.__dict__
    return new_module
