from flask import Blueprint, g
from . import app


class CanellaModule(Blueprint):
    """
    Namespaces canella related Blueprint to prevent conflict
    """
    def __init__(self, name, import_name, **kwargs):
        super(CanellaModule, self).__init__("canella-%s" %name, import_name, **kwargs)


class LanguageSelectorMiddleware(object):
    """
        See if the request path starts with a language code, in this case
        it will be assigned to a variable and removed from the request path.
    """
    def __init__(self, app):
        self.app = app

    def  __call__(self, environ, start_response):
        path = environ.get('PATH_INFO')
        if path:
            path = path.strip('/').split('/')
            if path[0] in ['en', 'ar']:
                environ['PATH_INFO'] = '/' + '/'.join(path[1:]) + '/'
        return self.app(environ, start_response)

app.wsgi_app = LanguageSelectorMiddleware(app.wsgi_app)
