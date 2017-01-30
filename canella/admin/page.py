from flask import url_for
from .. import db
from ..babel import gettext, lazy_gettext
from ..page.models import Page
from ..util.wtf import RichTextAreaField
from .core import DisplayableAdmin
from . import admin

class PageAdmin(DisplayableAdmin):
    form_rules = [(4, "content"), (5, "parent"), (6, "must_show_in_menu")]
    form_excluded_columns = ["children", "contenttype", "slug_path"]
    column_list = [(1, "parent")]
    form_overrides = {
        'content': RichTextAreaField
    }

    def edit_form(self, obj):
        return self.modify_edit_form(super(PageAdmin, self).edit_form(obj), page=obj)

    def modify_edit_form(self, form, page):
        form.parent.query_factory = Page.query.filter(Page.id != page.id).all
        return form

    def get_preview_url(instance):
        return url_for('canella-page.get_page_by_slug', slug=instance.slug_path)

admin.add_view(PageAdmin(Page, db.session, category=lazy_gettext('Pages'), name=lazy_gettext('Page')))