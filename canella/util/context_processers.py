from flask import request, url_for
from flask_admin import helpers as admin_helpers
from flask_babelex import get_locale
from .. import app, db
from ..main import security
from ..admin import admin
from ..settings import current_settings
from ..core.models import Site
from ..page.models import Page
from ..babel import gettext, ngettext
from .templating import should_enable_inline_editing

@app.context_processor
def enject_settings():
    return dict(settings=current_settings)

@app.context_processor
def inject_site():
    return dict(site=Site.query.filter(Site.is_active==True).one())

@app.context_processor
def enject_pages():
    pages = Page.query.viewable.filter(Page.is_primary==True).filter(Page.slug_path!=app.config.get('HOME_SLUG')).all()
    return dict(pages=pages)

@app.context_processor
def inject_should_enable_inline_editing():
    return dict(should_enable_inline_editing=should_enable_inline_editing())

@app.context_processor
def inject_language_info():
    lang = get_locale().language
    rtl = lang in ('ar', 'az', 'fa', 'he', 'ur', )
    return dict(lang=lang, rtl=rtl, _trans=gettext, _ntrans=ngettext)

@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for,
        _gettext= gettext,
        _trans= gettext
    )