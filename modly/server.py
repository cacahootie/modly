import os
from threading import Lock

from flask import Flask
from werkzeug.wsgi import pop_path_info, peek_path_info

import getters

class PathDispatcher(object):

    def __init__(self, cfg):
        self.cfg = { x['prefix']: x for x in cfg }
        self.default_app = default_app()
        self.lock = Lock()
        self.instances = {}

    def get_application(self, prefix):
        if prefix not in self.cfg:
            return
        with self.lock:
            app = self.instances.get(prefix)
            if app is None:
                app = self.create_app(prefix)
                if app is not None:
                    self.instances[prefix] = app
            return app

    def create_app(self, prefix):
        cfg = self.cfg[prefix]
        main = cfg['main'].split('.')
        modpath = '/'.join(main[:-1]) + '.py'
        mod = getters.get_github_module(
            cfg['user'], cfg['repo'], modpath, main[-2]
        )
        return getattr(mod, main[-1])

    def __call__(self, environ, start_response):
        app = self.get_application(peek_path_info(environ))
        if app is not None:
            pop_path_info(environ)
        else:
            app = self.default_app
        return app(environ, start_response)


def default_app():
    app = Flask('modly_fallback')

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        return "Sorry, but there's nothing there: {}".format(path), 404

    return app


def process_config(user, repo):
    config = getters.get_github_json(user, repo, 'config.json')
    if config is None:
        return
    config.update({
        "user": user,
        "repo": repo
    }) # i wish the impossible wish to update and return in a single exp...
    return config


def process_whitelist(user, repo):
    whitelist = getters.get_github_json(user, repo, 'whitelist.json')
    if whitelist is None:
        return
    return [
        process_config(**i)
        for i in whitelist
    ]


def get_instance(user=None, repo=None):
    if user is None:
        user = user or os.environ.get('GH_USER') or 'cacahootie'
        repo = repo or os.environ.get('GH_REPO') or 'modly-test'
    cfg = process_whitelist(user, repo)\
        or [process_config(user, repo)]
    return PathDispatcher(cfg)
