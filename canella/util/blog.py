from flask import request, url_for
from werkzeug.contrib.atom import AtomFeed
from jinja2.utils import Markup
from ..core.models import Site
from ..blog.models import Post
from ..settings import current_settings as settings


def make_summary(content, p=3):
    return ' '.join(Markup(content).striptags().split('.')[:p])

def make_blog_feed(order=None, limit=15):
    feed = AtomFeed(
        title="{} - Blog Feed".format(settings.title),
        subtitle=settings.tagline,
        feed_url=request.url,
        url=request.url_root,
        author="Musharraf Omer",
        icon=None,
        logo=None,
        rights="Copyright 2000-2016 - Mushy.ltd",
    )
    order = order or Post.publish_date.desc()
    items = Post.query.order_by(order).limit(limit).all()
    for item in items:
        item.url = url_for('canella-blog.post', slug=item.slug)
        feed.add(
            title=item.title,
            url=item.url,
            content=make_summary(item.body),
            content_type='html',
            summary=item.meta_description,
            updated=item.updated or item.created,
            author="Musharraf Omer",
            published=item.publish_date,
            categories=[{'term': t.slug, 'label': t.title} for t in item.tags]
        )
    return feed

