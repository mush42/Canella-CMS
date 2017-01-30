from collections import OrderedDict
from .. import app
from ..babel import lazy_gettext
from ..util.option import Option

"""
Default, Editable, settings for each new site
Define your editable setting like this:
    'setting_key': {'label':'A Label', 'description':'A Desc', 'category':'general', type=int, 'choices':[], 'default'='value'}
"""

DEFAULT_CATEGORIES = OrderedDict()
DEFAULT_CATEGORIES['general'] = dict(label=lazy_gettext('General'), icon='fa-cog')
DEFAULT_CATEGORIES['blog'] = dict(label=lazy_gettext('Blog'), icon='')

DEFAULT_SETTINGS = (
    Option('enable_comments',
        label=lazy_gettext('Enable Comments'),
        description=lazy_gettext('Enable comments on blog posts'),
        category='blog',
        type='checkbox',
        default=True),
    Option('auto_approve_comments',
        label=lazy_gettext('Auto Approve Comments'),
        description=lazy_gettext('Comments will be published without the need for Approval'),
        category='blog',
        type='checkbox',
        default=True),
    Option('title',
        label=lazy_gettext('Site Title'),
        description=lazy_gettext('The site Title'),
        category='general',
        type='text',
        default='Canella CMS'),
    Option('tagline',
        label=lazy_gettext('Site Tag Line'),
        description=lazy_gettext('The sub-title of the site'),
        category='general',
        type='text',
        default='A Free, Open Source Content Management System Built With Flask'),
    Option('tweet_new_posts',
        label=lazy_gettext('Tweet New Posts'),
        description=lazy_gettext(' New post will be tweeted'),
        category='blog',
        type='checkbox',
        default=False),
    Option('posts_per_page', 
        label=lazy_gettext('Posts per page'),
        description=lazy_gettext('Number of posts per one page'),
        category='blog',
        type='number',
        default=5),
)
