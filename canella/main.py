from flask import request, session, g, abort
from flask_security import Security, SQLAlchemyUserDatastore, current_user
from . import app, db, babel

from .core import core
from .page import page
from .blog import blog
from .user import user
from .files import files
from .settings import settings
from .api import api_bp
from .user.models import User, Role
from .form.models import *
from .util.forms.login import CanellaLoginForm
from .util.forms.recover import CanellaRecoverPasswordForm

for blueprint in (core, page, blog, settings, files, user, api_bp):
    app.register_blueprint(blueprint)


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(
    app, user_datastore,
    login_form=CanellaLoginForm,
    forgot_password_form=CanellaRecoverPasswordForm
)

@app.before_request
def security_processer():
    if not request.blueprint == 'security':
        return
    if request.endpoint == 'security.login':
            form = CanellaLoginForm()
            if form.validate_on_submit():
                session['lang'] = form.lang.data
    elif request.endpoint == 'security.logout' and 'lang' in session:
        session.pop('lang')


@babel.localeselector
def get_locale():
    lang = request.args.get('lang')
    if current_user.is_authenticated:
        profile_data = current_user.profile or {}
        lang = lang or profile_data.get('language')
    lang = lang or session.get('lang')
    supported_langs = app.config['DEFAULT_LOCALE']
    if lang and lang in supported_langs:
        return lang
    return request.accept_languages.best_match(supported_langs)

# Admin
from .admin import *
# API
from .api.core import *
from .api.blog import *
from .api.page import *
from .api.settings import *
from .api.user import *
from .api.media import *

# Utilities
from .admin import *
from .admin.settings import *
from .events import *
from .util.context_processers import *
from .util.commands import *
from .util.templating import *
