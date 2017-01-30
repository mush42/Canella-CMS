from flask import request, flash, url_for, redirect
from flask_admin import BaseView, expose
from flask_security import current_user
from flask_wtf import Form
from sqlalchemy.exc import SQLAlchemyError

from .. import app, db
from ..babel import gettext, lazy_gettext
from ..core.models import Site
from ..settings import current_settings
from ..util.dynamicform import DynamicForm
from . import admin, AuthenticationViewMixin

def make_settings_form(category):
    fields = []
    settings = Site.query.filter(Site.is_active==True).one().settings
    for option in list(current_settings.options):
        if option.category != category:
            continue
        option.default = settings[option.name]
        fields.append(option)
    return DynamicForm(*fields, with_admin=True).form

def update_settings_from_form(data):
    for k, v in data.items():
        current_settings.edit(k, v)

@app.before_first_request
def add_settings_categories():
    categories = current_settings.categories.items()
    for category, info in categories:
        class SettingsAdmin(AuthenticationViewMixin, BaseView):
            settings_category = category
            @expose('/', methods=['Get', 'POST'])
            def index(self):
                form = make_settings_form(category=self.settings_category)
                if form.validate_on_submit():
                    update_settings_from_form(form.data)
                    flash("Settings were successfully saved")
                    return redirect(request.url)
                return self.render('canella/admin/settings.html', form=form)

        admin.add_view(SettingsAdmin(
            name=info['label'],
            menu_icon_type='fa',
            menu_icon_value=info['icon'],
            category=gettext("Settings"),
            endpoint="admin-settings-{}".format(category),
            url="settings/{}".format(category)
        ))
