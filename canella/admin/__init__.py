from flask import request, redirect
from flask_admin import Admin, expose
from flask_admin.base import BaseView, AdminIndexView
from flask_admin.form import SecureForm
from flask_admin.contrib.sqla import ModelView, form
from flask_security import current_user
from .. import app, db
from ..babel import gettext, ngettext, lazy_gettext

class AuthenticationViewMixin(object):
    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        if current_user.has_role('admin'):
            return True
        return False

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            if current_user.is_authenticated:
                abort(403)
            else:
                return redirect(url_for('security.login', next=request.url))

class CanellaModelFormConvertor(form.AdminModelConverter):
    def _get_label(self, name, field_args):
        info = getattr(self.view.model, name).info
        if info.get('label'):
            return info['label']
        return super(CanellaModelFormConvertor, self)._get_label(name, field_args)

    def _get_description(self, name, field_args):
        info = getattr(self.view.model, name).info
        if info.get('description'):
            return info['description']
        return super(CanellaModelFormConvertor, self)._get_description(name, field_args)


class CanellaModelView(AuthenticationViewMixin, ModelView):
    """Automatic authentication and some extras"""
    model_form_converter = CanellaModelFormConvertor
    def get_column_name(self, field):
        if self.column_labels and field in self.column_labels:
            return self.column_labels[field]
        column = self.model.__mapper__.columns.get(field)
        if column is not None and column.info.get('label'):
            return column.info['label']
        return super(CanellaModelView, self).get_column_name(field)

class CanellaIndexView(AuthenticationViewMixin, AdminIndexView):
    @expose('/')
    def index(self):
        cards = dict()
        cards['comments'] = dict()
        cards['comments']['heading'] = 'Comments'
        cards['comments']['icon'] = 'fa fa-comment'
        cards['comments']['link'] = 'http://localhost:8000'
        self._template_args['cards'] = cards
        return super(CanellaIndexView, self).index()

index_view = CanellaIndexView(menu_icon_type='fa', menu_icon_value='fa-home', template='canella/admin/index.html')

admin = Admin(
    app, name=lazy_gettext('Dashboard'),
    template_mode='bootstrap3', base_template='canella/admin/layout.html',
    index_view=index_view,
    category_icon_classes={'Settings': 'fa fa-cog', 'Pages':'fa fa-file-text-o', 'Users': 'fa fa-users', 'Blog': 'fa fa-link'}
)

from .core import *
from .blog import *
from .page import *
from .user import *
from .files import *
from .form import *