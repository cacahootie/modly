from threading import Lock

from flask import Flask
from werkzeug.wsgi import pop_path_info, peek_path_info

import getters

class PathDispatcher(object):

    def __init__(self, create_app):
        self.create_app = create_app
        self.default_app = default_app()
        self.lock = Lock()
        self.instances = {}

    def get_application(self, prefix):
        with self.lock:
            app = self.instances.get(prefix)
            if app is None:
                app = self.create_app(prefix)
                if app is not None:
                    self.instances[prefix] = app
            return app

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


def make_app(prefix):
    mod = getters.get_github_module(
        'cacahootie', 'modly', 'test/modly-test/models.py', 'models'
    )
    return mod.app


def get_instance():
    return PathDispatcher(make_app)
