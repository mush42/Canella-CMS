import os
from collections import OrderedDict
from canella import app
from canella.babel import lazy_gettext


_BASEDIR = app.root_path

HOME_SLUG = 'index'
DB_DIR = os.path.join(_BASEDIR, '..', '.ignore.local', 'data.db')
DEBUG = True
SECRET_KEY = '9bW7b2046be56b4c00b6f10dc2f3c4Ae56SL5PC9'
SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(DB_DIR)
SQLALCHEMY_TRACK_MODIFICATIONS = False
ERROR_404_HELP = False
CONTENT_PATH = os.path.join(_BASEDIR, 'uploads', 'content')
MEDIA_PATH = os.path.join(_BASEDIR, 'uploads', 'media')
FORM_UPLOADS_PATH = os.path.join(_BASEDIR, 'uploads', 'forms')
SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
SECURITY_PASSWORD_SALT = '540SDW4426HCAER56546aDrw213d2a6b9a94e15b5d'
SECURITY_USER_IDENTITY_ATTRIBUTES = ['email', 'user_name']
SECURITY_POST_LOGIN_VIEW = '/admin'
SECURITY_CONFIRMABLE = False
SECURITY_RECOVERABLE = True
SECURITY_RESET_URL = '/reset-password/'
ALLOWED_EXTENSIONS = ['doc', 'docx', 'ppt', 'pptx', 'pdf', 'zip']
ENABLE_INLINE_EDITING = True
SUPPORTED_LOCALES = OrderedDict((
    ('en', 'English'),
    ('ar', 'Arabic')
))
DEFAULT_LOCALE = 'en'
BABEL = dict(
    domain='canella',
    translations_directory=os.path.join(_BASEDIR, 'translations'),
    babel_config=os.path.abspath(os.path.join(_BASEDIR, '..', 'babel', 'babel.cfg')),
    catalog_output_path=os.path.abspath(os.path.join(_BASEDIR, '..', 'babel')),
    catalog_filename=os.path.abspath(os.path.join(_BASEDIR, '..', 'babel', 'canella.pot')),
    project_name='Canella-CMS',
)

# Add extra fields you want to add to the profile here
PROFILE_EXTRA_FIELDS = (
    dict(name='language',
        label=lazy_gettext('Default Site Language'),
        description=lazy_gettext('All the site elements will be displayed in this language'),
        type='select',
        choices=lambda: app.config['SUPPORTED_LOCALES'].items(),
        default=lambda: app.config['DEFAULT_LOCALE']),
    dict(name='facebook_profile',
        label=lazy_gettext('Facebook Profile'),
        description=lazy_gettext('Will be displayed beneeth your bio in some places'), type='url', default=''),
    dict(name='twitter_account',
        label=lazy_gettext('Twitter Page URL'),
        description=lazy_gettext('Will be displayed beneeth your bio in some places'), type='url', default=''),
)
