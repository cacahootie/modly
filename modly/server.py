import os
from threading import Lock

from flask import Flask
from werkzeug.wsgi import pop_path_info, peek_path_info

import getters, fallback
from configurator import process_config, process_whitelist


class PathDispatcher(object):

    def __init__(self, cfg):
        self.cfg = { x['prefix']: x for x in cfg }
        self.default_app = fallback.default_app
        self.lock = Lock()
        self.instances = {}

    def get_application(self, environ):
        prefix = pop_path_info(environ)
        if prefix not in self.cfg:
            return None, None
        branch = peek_path_info(environ)
        with self.lock:
            if (prefix, branch) not in self.instances and branch not in self.instances:
                app = self.create_app(prefix, branch)
                if app:
                    self.instances[(prefix, branch)] = app
                else:
                    self.create_app(prefix)
                    self.instances[prefix] = app

            if (prefix, branch) in self.instances:
                app = self.instances[(prefix, branch)]
                pop_path_info(environ)
            else:
                app = self.instances[prefix]
            return app

    def _process_main(self, prefix):
        cfg = self.cfg[prefix]
        main = cfg['main'].split('.')
        modpath = '/'.join(main[:-1]) + '.py'
        return modpath, main[-2], main[-1]

    def create_app(self, prefix, branch):
        cfg = self.cfg[prefix]
        modpath, modname, appname = self._process_main(prefix)
        mod = getters.get_github_module(
            cfg['user'], cfg['repo'], modpath, modname, branch
        )
        return mod, getattr(mod, appname) # flask-voodoo!!!

    def __call__(self, environ, start_response):
        mod, app = self.get_application(environ)
        if any((mod is None, app is None)):
            app = self.default_app
        return app(environ, start_response)


def get_instance(user=None, repo=None):
    if user is None:
        user = user or os.environ.get('GH_USER') or 'cacahootie'
        repo = repo or os.environ.get('GH_REPO') or 'modly-test'
    cfg = process_whitelist(user, repo)\
        or process_config(user, repo)
    return PathDispatcher(cfg)
