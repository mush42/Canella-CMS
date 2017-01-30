from collections import OrderedDict
from werkzeug.local import LocalProxy
from ..wrappers import CanellaModule
from .models import *
from ..babel import lazy_gettext
from .defaults import DEFAULT_SETTINGS, DEFAULT_CATEGORIES


settings = CanellaModule(
    'settings', __name__)

class Settings(object):
    def __init__(self, source):
        self.source = source
        self.options = []
        self.categories = OrderedDict()
        for name, kwargs in DEFAULT_CATEGORIES.items():
            self.register_category(name, **kwargs)
        for option in DEFAULT_SETTINGS:
            self.register_setting(option)

    def register_setting(self, option):
        assert option.name not in [option.name for option in self.options], '%s is already registered' %option.name
        if not option.category:
            option.category = self.categories['general']
        elif option.category not in self.categories:
            raise ValueError('category %s does not exists, please register it first' %option.category)
        self.options.append(option)
        if option.name not in self.source:
            self.edit(option.name, option.default, new=True)

    def register_category(self, name, label, icon=''):
        if name in self.categories:
            raise ValueError('%s category already registered' %name)
        self.categories[name] = dict(label=label, icon=icon)

    def __getattr__(self, key):
        if key in self.source:
            return self.source[key]

    def edit(self, key, value, new=False):
        if key not in [option.name for option in self.options]:
            raise ValueError('Setting %s is not registered yet' %key)
        if not new and key not in self.source:
            raise AttributeError('%r has no attribute %r' %(self.source, key))
        self.source[key] = value
        db.session.commit()

def get_active_site():
    from ..core.models import Site
    active_site = Site.query.filter(Site.is_active==True).one()
    return active_site

current_site = LocalProxy(lambda: get_active_site())
current_settings = LocalProxy(lambda: Settings(get_active_site().settings))
