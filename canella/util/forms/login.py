from flask_security.forms import LoginForm
from wtforms.fields import StringField, SelectField, PasswordField
from wtforms.validators import data_required
from ... import app
from ...babel import lazy_gettext

class EmailFormMixin(object):
    email = StringField(
        label=lazy_gettext('Email or Username'),
        validators=[data_required()],
        render_kw=dict(required=True)
    )

class PasswordFormMixin(object):
    password = PasswordField(
        label=lazy_gettext('Password'),
        validators=[data_required()],
        render_kw=dict(required=True)
    )

class CanellaLoginForm(EmailFormMixin, PasswordFormMixin, LoginForm):
    lang = SelectField(
        label=lazy_gettext('Dashboard Language'),
        choices=app.config['SUPPORTED_LOCALES'].items(),
        validators=[data_required()],
        render_kw=dict(required=True)
    )

