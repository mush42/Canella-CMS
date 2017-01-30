from sqlalchemy import func
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property
from flask_sqlalchemy import BaseQuery
from flask_security import current_user
from datetime import datetime
from .. import db
from ..babel import lazy_gettext
from ..settings import current_site
from ..util.slugging import slugify

class Titled(object):
    title = db.Column(db.Unicode(255), nullable=False,
    info=dict(label=lazy_gettext('Title'), description=lazy_gettext('The title to display in the browser title bar.'))
)

    def __str__(self):
        return self.title
    __unicode__ = __str__

    def __repr__(self):
        return '{0}(title={1})'.format(self.__class__.__name__, self.title)

class Slugged(object):
    slug = db.Column(
        db.Unicode(255),
        info=dict(label=lazy_gettext('Slug'), description=lazy_gettext('A Slug is that portion of the URL used to identify this content.'))
    )

class UniquelySlugged(Slugged):
    slug = db.Column(
        db.Unicode(255),
        unique=True, index=True,
        info=dict(label=lazy_gettext('Slug'), description=lazy_gettext('A Slug is that portion of the URL used to identify this content.'))
    )

class Metadata(object):
    meta_title = db.Column(db.Unicode(255),
        info=dict(label=lazy_gettext('Meta Title'), description=lazy_gettext('The title used by search engines'))
    )
    meta_description = db.Column(db.UnicodeText,
        info=dict(label=lazy_gettext('Meta Description'), description=lazy_gettext('The description used by search engines'))
    )
    has_auto_desc = db.Column(db.Boolean, default=True,
        info=dict(label=lazy_gettext('Enable Auto Description'), description=lazy_gettext('If enabled the meta description will be generated automaticly'))
    )
    keywords = db.Column(db.Text, 
        info=dict(label=lazy_gettext('Keywords'), description=lazy_gettext('The keywords for this content (Used by search engines)'))
    )

class TimeStampped(object):
    created = db.Column(db.DateTime, default=func.now(), nullable=False,
        info=dict(label=lazy_gettext('Creation Date'))
    )
    updated = db.Column(db.DateTime, default=func.now(), onupdate=func.now(), nullable=False,
        info=dict(label=lazy_gettext('Last Updated'))
    )

class Publishable(object):
    STATUS_CHOICES = [
        ('published', lazy_gettext('Published')),
        ('draft', lazy_gettext('Draft')),
        ('expired', lazy_gettext('Expired')),
    ]
    status = db.Column(
        db.Enum(*[value for value, label in STATUS_CHOICES]),
        default=STATUS_CHOICES[0][0],
        info=dict(choices=STATUS_CHOICES, label=lazy_gettext('Status'), description=lazy_gettext('The status of this content. Draft content will not be shown.'))
    )
    publish_date = db.Column(db.DateTime, default=func.now(), nullable=False,
        info=dict(label=lazy_gettext('Publish Date'), description=lazy_gettext('The content will not be publish until this date.'))
    )
    expire_date = db.Column(db.DateTime,
        info=dict(label=lazy_gettext('Expiration Date'), description=lazy_gettext('The content will not be publish After this date.'))
    )

    @hybrid_property
    def is_published(self):
        rv = self.status == self.STATUS_CHOICES[0][0] and self.publish_date <= datetime.now()
        if self.expire_date is not None:
            rv = rv and self.expire_date >= datetime.now()
        return rv


class Site(UniquelySlugged, db.Model):
    __slugcolumn__ = 'name'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(255), unique=True, nullable=False,
        info=dict(label=lazy_gettext('Site Name'), description=lazy_gettext('Unique name to identify this site.'))
    )
    is_active = db.Column(db.Boolean, default=False,
        info=dict(label=lazy_gettext('Active By Default'), description=lazy_gettext('The default site for urls'))
    )
    settings = db.relationship('Settings', backref="site", uselist=False)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "Site(name='{}')".format(self.name)

class DisplayableQuery(BaseQuery):
    @property
    def published(self):
        pub = self._joinpoint_zero().columns['publish_date']
        expire = self._joinpoint_zero().columns['expire_date']
        rv = self.filter_by(status='published').filter(pub<=datetime.now())
        if expire is not None:
            rv.filter(expire>=datetime.now())
        return rv

class Displayable(db.Model, Titled, Slugged, Metadata, TimeStampped, Publishable):
    """Displayable"""
    __abstract__ = True
    __slugcolumn__ = 'title'
    query_class = DisplayableQuery

    @declared_attr
    def __versioned__(cls):
        return {
            'exclude': ['created']
        }

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @declared_attr
    def user_id(cls):
        return db.Column(
            db.Integer,
            db.ForeignKey('user.id'), nullable=False,
            default=lambda c: current_user.id if current_user and current_user.is_authenticated else 1,
            onupdate=lambda c: current_user.id if current_user and current_user.is_authenticated else 1,
            info=dict(label=lazy_gettext('Author'))
            )

    @declared_attr
    def author(cls):
        return db.relationship('User',
            info=dict(label=lazy_gettext('Author'), description=lazy_gettext(''))
            )

    @declared_attr
    def site_id(cls):
        return db.Column(
            db.Integer,
            db.ForeignKey('site.id'), nullable=False,
            default=lambda c: current_site.id,
            info=dict(label=lazy_gettext('Site'))
            )

    @declared_attr
    def site(cls):
        return db.relationship('Site',
            info=dict(label=lazy_gettext('Site'), description=lazy_gettext('The site to wich this content will be published'))
        )

db.DisplayableBase = Displayable