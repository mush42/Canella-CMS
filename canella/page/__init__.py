from flask import request, make_response, g, render_template, url_for, abort
from warnings import warn
from .. import app
from ..wrappers import CanellaModule
from .models import Page
from ..util.page import render_page_template
from .. import db
    
def get_page(slug_path):
    return Page.query.published.filter(Page.slug_path==slug_path).one_or_none()

def set_g_page():
    slug = request.path.strip('/')
    if not slug:
        slug = app.config.get('HOME_SLUG', 'index')
    slug_path = slug.split('/')
    while slug_path:
        g.page = get_page('/'.join(slug_path))
        if g.page:
            break
        slug_path.pop(-1)
    if g.page:
        setattr(g, g.page.__contenttype__, g.page)

class PageBlueprint(CanellaModule):
    _page_handlers = {}
    def __init__(self, name, importname, **kwargs):
        super(PageBlueprint, self).__init__(name, importname, **kwargs)
        self.before_request(set_g_page)

    def add_handler(self, func, contenttype, methods):
        self._page_handlers[contenttype] = (func, methods)

    def get_handler_for(self, key):
        return self._page_handlers.get(key)

    def handler(self, contenttype, methods):
        def wrapper(func):
            self.add_handler(func, contenttype, methods)
            def wrapped(*a, **kw):
                return func(*a, **kw)
            return wrapped
        return wrapper

page = PageBlueprint('page', __name__)

@page.before_app_first_request
def warn_if_home_does_not_exist():
    if get_page(app.config.get('HOME_SLUG', 'index')) is None:
        warn('Home page is not defined, your visitors will see a 404 error when they visit your site root')

@page.route('/<slug:slug>', endpoint='get_page_by_slug', methods=['GET', 'POST'])
def page_view(slug):
    if not g.page:
        abort(404)
    handler = page.get_handler_for(g.page.contenttype)
    template_args = {}
    if handler is not None:
        if request.method not in handler[1]:
            abort(405)
        rv = handler[0]()
        if isinstance(rv, dict):
            template_args.update(rv)
        else:
            return rv
    return render_page_template(context=template_args)

@page.route('/', endpoint='index')
def index():
    if not g.page:
        abort(404)
    return render_page_template()
