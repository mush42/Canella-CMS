from flask import url_for
from flask_admin import form
from flask_admin.model.form import InlineFormAdmin
from flask_admin.form import rules
from flask_admin.form.fields import Select2TagsField
from jinja2 import Markup
from wtforms.widgets import HiddenInput
from wtforms.fields import StringField

from .. import app, db
from ..babel import gettext, lazy_gettext
from ..blog.models import Post, Tag, Category, Comment
from ..util.wtf import RichTextAreaField, FileSelectorField
from . import admin, CanellaModelView
from .core import DisplayableAdmin


class BlogPostAdmin(DisplayableAdmin):
    column_editable_list = ["status"]
    form_excluded_columns= ["comments", 'author', 'tags']
    form_rules= [
        (5, "image_path"), (6, "image_description"), (7, "category"),
        (8, "body"), (9, "enable_comments"),
    ]
    form_overrides = {
        'body': RichTextAreaField,
    }
    form_extra_fields = {
        'image_path': FileSelectorField(label=lazy_gettext('Featured Image'), button_text=lazy_gettext('Select Featured Image'), filters=[lambda i: i or None]),
    }
    
    def get_preview_url(instance):
        return url_for('canella-blog.post', slug=instance.slug)

class CategoryAdmin(CanellaModelView):
    form_excluded_columns = ['posts']
    column_list = ['title', 'slug']
    column_editable_list = ['title', 'slug']
    
class CommentAdmin(CanellaModelView):
    column_editable_list = ['author_name', 'author_email', 'body']

admin.add_view(BlogPostAdmin(Post, db.session, name=lazy_gettext('Posts'), category=lazy_gettext('Blog'), menu_icon_type='fa', menu_icon_value='fa-newspaper-o'))
admin.add_view(CategoryAdmin(Category, db.session, name=lazy_gettext('Categories'), category=lazy_gettext('Blog'), menu_icon_type='fa', menu_icon_value='fa-tags'))
admin.add_view(CommentAdmin(Comment, db.session, name=lazy_gettext('Comments'), category=lazy_gettext('Blog'), menu_icon_type='fa', menu_icon_value='fa-comment'))

