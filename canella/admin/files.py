from flask import request, url_for
from flask_admin import expose
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin import form
from jinja2 import Markup
from .. import app
from ..babel import gettext, lazy_gettext
from . import admin, AuthenticationViewMixin

class MediaLibraryAdmin(AuthenticationViewMixin, FileAdmin):
    can_delete_dirs = False
    can_mkdir = False
    can_rename = False
    allowed_extensions = {'jpg', 'png', 'gif', 'svg', 'ico', 'mp3', 'mp4', 'webma', 'm4a', 'flv'}
    list_template = 'canella/admin/files/media-list.html'

class ContentFileAdmin(AuthenticationViewMixin, FileAdmin):
    rename_modal = True
    allowed_extensions = app.config.get('ALLOWED_EXTENSIONS', [])


admin.add_view(MediaLibraryAdmin(app.config['MEDIA_PATH'], base_url='/media/', name=lazy_gettext('Media Library'), url='media', endpoint='media', menu_icon_type='fa', menu_icon_value='fa-image'))
admin.add_view(ContentFileAdmin(app.config['CONTENT_PATH'], base_url='/content/', name=lazy_gettext('Content'), url='content', menu_icon_type='fa', menu_icon_value='fa-folder'))