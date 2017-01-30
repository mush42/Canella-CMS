from flask import url_for
from sqlalchemy import Table, func
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from .. import db
from ..babel import lazy_gettext
from ..core.models import Titled, UniquelySlugged, Displayable
from ..files.models import ImageMixin
from ..settings import current_settings

posts_tags = Table('posts_tags', db.Model.metadata,
    db.Column('post_id', db.ForeignKey('post.id'), primary_key=True),
    db.Column('tag_id', db.ForeignKey('tag.id'), primary_key=True)
)

class PostBase(db.DisplayableBase):
    __abstract__ = True
    body = db.Column(db.Text,
        info=dict(label=lazy_gettext('Body'), description=lazy_gettext('Content body.'), markup=True, markup_type='html')
    )


class Tag(Titled, UniquelySlugged, db.Model):
    __slugcolumn__ = 'title'
    id = db.Column(db.Integer, primary_key=True)
    posts = db.relationship(
        'Post', secondary=posts_tags,
        back_populates='tags', lazy="dynamic")


class Category(Titled, UniquelySlugged, db.Model):
    __slugcolumn__ = 'title'
    id = db.Column(db.Integer, primary_key=True)
    posts = db.relationship("Post", back_populates="category", lazy="dynamic")


class Post(UniquelySlugged, PostBase, ImageMixin):
    id = db.Column(db.Integer, primary_key=True)
    enable_comments = db.Column(db.Boolean, default=True,
        info=dict(label=lazy_gettext('Enable Comments'), description=lazy_gettext('Toggle visitors comments in this post. '))
    )
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False,
        info=dict(label=lazy_gettext('Category'))
    )
    category = db.relationship("Category", back_populates="posts",
        info=dict(label=lazy_gettext('Category'), description=lazy_gettext('The category under wich this post will be published.'))
    )
    comments = db.relationship("Comment", backref="post")
    tags  = db.relationship('Tag',
        secondary=posts_tags,
        back_populates='posts', collection_class=set,
        info=dict(label=lazy_gettext('Post Tags'), description=lazy_gettext('Add tags to group posts by topic'))
    )
    tag_list = association_proxy(
        'tags', 'title',
        creator=lambda title: Tag(title=title))


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(db.Unicode(255), nullable=False,
        info=dict(label=lazy_gettext('Your Name'), description=lazy_gettext(''))
    )
    author_email = db.Column(db.Unicode(255), nullable=False,
        info=dict(label=lazy_gettext('Your Email'), description=lazy_gettext(''))
    )
    publish_date = db.Column(db.DateTime, default=func.now())
    body = db.Column(db.Text, nullable=False,
        info=dict(label=lazy_gettext('Your Comment'), description=lazy_gettext(''))
    )
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False,
        info=dict(label=lazy_gettext('Post'))
    )
    approved = db.Column(db.Boolean, default=lambda c: current_settings.auto_approve_comments,
        info=dict(label=lazy_gettext('Approved'))
    )