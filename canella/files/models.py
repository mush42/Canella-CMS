import os
from collections import namedtuple
from flask import url_for
from sqlalchemy.ext.declarative import declared_attr
from .. import app, db
from ..babel import lazy_gettext

class ImageMixin(object):
    @declared_attr
    def image_path(cls):
        return db.Column(db.UnicodeText)
    
    @declared_attr
    def image_description(cls):
        return db.Column(db.UnicodeText,
            info=dict(label=lazy_gettext('Image Description'), description=lazy_gettext('If supplying an image please provide a description for the purposes  of ACCESSIBILITY and SEO'))
        )

    @property
    def image(self):
        info = namedtuple('info', 'src description')
        return info(url_for('canella-files.media', filename=self.image_path), self.image_description)