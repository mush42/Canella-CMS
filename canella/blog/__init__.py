from flask import request, flash, g, url_for, redirect, abort
from flask_security import current_user
from flask_wtf import Form
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, Email
from .models import Post, Tag, Category, Comment
from .. import app, db
from ..babel import gettext
from ..page import PageBlueprint
from ..user.models import User
from ..settings import current_settings
from ..util.blog import make_blog_feed
from ..util.page import render_page_template
from ..util.dynamicform import DynamicForm

blog = PageBlueprint('blog', __name__, url_prefix='/blog')

def filter_by_user(q):
    if not current_user.is_authenticated or not current_user.is_active or not current_user.has_role('admin'):
        q = q.published
    return q

def create_comment_form():
    name, email = getattr(current_user, 'name', ''), getattr(current_user, 'email', '')
    fields = (
        dict(name='author_name', label=gettext('Your Name'), required=True, type='text', default=name),
        dict(name='author_email', label=gettext('Your Email'), required=True, type='email', default=email),
        dict(name='body', label=gettext('Your Comment'), required=True, type='textarea'),
    )
    return DynamicForm(*fields).form

@blog.route('/', endpoint="listing")
def blog_view(q=None, extra_context=None):
    page = int(request.args.get("page", 1))
    item_count = current_settings.posts_per_page
    if q is None:
        q = Post.query
    q = filter_by_user(q)
    post_paginator = q.order_by(Post.publish_date.desc()).paginate(page, item_count, False)
    context = {
        "posts": post_paginator.items,
        'paginator':post_paginator,
    }
    context.update(extra_context or {})
    return render_page_template(
        page=g.page,
        context=context,
        template="site/blog/listing.html"
    )

@blog.route('/<slug>/', endpoint="post", methods=['Get', 'POST'])
def post_view(slug):
    q = filter_by_user(Post.query.filter(Post.slug==slug))
    post = q.one_or_none()
    if post is None:
        return render_page_template(
        context={"post": None},
        template="site/blog/post.html"
        )
    form = Form()
    if post.enable_comments and current_settings.enable_comments:
        form = create_comment_form()
        if form.validate_on_submit():
            post.comments.append(Comment(**form.data))
            db.session.commit()
            flash("Your comment was sent")
            return redirect(url_for('canella-blog.post', slug=post.slug))
    return render_page_template(
        context={"post": post, 'comment_form':form},
        template="site/blog/post.html"
    )

@blog.route('/feed.xml')
def feed():
    return make_blog_feed().get_response()

@blog.route('/<attr_name>/<slug>/', endpoint='post_filter')
def filter_blog_posts(attr_name, slug):
    attr_map = {
        'author': (User, Post.query.join(User).filter(User.slug==slug)),
        'tag': (Tag, Post.query.filter(Post.tag_list.any(slug=slug))),
        'category': (Category, Post.query.join(Category).filter(Category.slug==slug)),
    }
    attr = attr_map.get(attr_name, None)
    if attr is None:
        abort(404)
    target = attr[0].query.filter_by(slug=slug).one_or_none()
    q = attr[1]
    return blog_view(q, extra_context={'target':target})
