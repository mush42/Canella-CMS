from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property
from .. import app, db
from ..babel import lazy_gettext
from ..core.models import Displayable, DisplayableQuery

class PageQuery(DisplayableQuery):
    @property
    def viewable(self):
        return self.published.filter_by(must_show_in_menu=True)

class PageBase(db.DisplayableBase):
    __abstract__ = True
    query_class = PageQuery
    slug_path = db.Column(db.Unicode(255), unique=True, index=True)
    
    @declared_attr
    def contenttype(cls):
        return db.Column(db.String(50),
            info=dict(label=lazy_gettext('Content Type'))
            )

    @declared_attr
    def must_show_in_menu(cls):
        return db.Column(db.Boolean, default=True,
            info=dict(label=lazy_gettext('Show in menu'), description=lazy_gettext('Show this page in the navigation menus.'))
        )

    @declared_attr
    def parent_id(cls):
        return db.Column(db.Integer, db.ForeignKey(cls.id),
            info=dict(label=lazy_gettext('Parent'))
            )
    
    @declared_attr
    def children(cls):
        return db.relationship(cls,
            info=dict(label=lazy_gettext('Children'), description=lazy_gettext(''))
        )
    
    @declared_attr
    def parent(cls):
        return db.relationship(cls, remote_side=cls.id,
            info=dict(label=lazy_gettext('Parent Page'), description=lazy_gettext('Parent page'))
        )

    @declared_attr
    def content(cls):
        return db.Column(db.UnicodeText, nullable=False,
            info=dict(label=lazy_gettext('Content'), description=lazy_gettext('Page content'), markup=True, markup_type='html')
        )

    @declared_attr
    def __mapper_args__(cls):
        return {
            'polymorphic_identity': cls.__contenttype__,
            'polymorphic_on': cls.contenttype
        }

    @property
    def url(self):
        return '/{}/'.format(self.slug_path)

    @hybrid_property
    def is_home(self):
        return self.slug == app.config['HOME_SLUG']

    @hybrid_property
    def is_primary(self):
        return self.parent_id == None

    def __str__(self):
        return self.title
    
    def __repr__(self):
        return "{0}(title='{1}')".format(self.__class__.__name__, self.title)

db.PageBase = PageBase

class Page(db.PageBase):
    __contenttype__ = 'page'
    id = db.Column(db.Integer, primary_key=True)
