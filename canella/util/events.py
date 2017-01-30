from sqlalchemy import inspect
from sqlalchemy.orm import attributes
from .. import db
from ..settings.models import Setting, Settings
from ..user.models import Profile
from ..settings import DEFAULT_SETTINGS
from .slugging import slugify
from .blog import make_summary

def select_instances_of_type(model, iter):
    for instance in iter:
        if not isinstance(instance, model):
            continue
        session = inspect(instance).session
        if not session.is_modified(instance, passive=True):
            continue
        yield instance

def edit_slug_path(old_slug_path, new_slug, index):
    slug_path = old_slug_path.split('/')
    slug_path[index] = new_slug
    return '/'.join(slug_path)

def recurcivly_change_slug_path(instance, slug, index=-1):
    with db.session.no_autoflush:
        instance.slug_path = edit_slug_path(instance.slug_path, slug, index)
        if instance.children:
            for child in instance.children:
                recurcivly_change_slug_path(child, slug, index=index-1)

def change_slug_path(instance):
    recurcivly_change_slug_path(instance, instance.slug)

def set_slug_path(instance):
    instance.slug = instance.slug or slugify(getattr(instance, instance.__slugcolumn__))
    slugs = [instance.slug]
    parent = instance.parent
    while parent is not None:
        slugs.append(parent.slug)
        parent = parent.parent
    instance.slug_path = '/'.join(reversed(slugs))
    if instance.children:
        for child in instance.children:
            set_slug_path(child)

def ensure_singlten_is_active(instance):
    """Make sure that one and only one site is active at the time"""
    if instance.is_active:
        with db.session.no_autoflush:
            site = instance.__class__
            active_sites = site.query.filter(site.is_active==True).all()
            for active_site in active_sites:
                active_site.is_active = False

def set_unique_slug(instance):
    insp = inspect(instance)
    if insp.persistent or insp.detached:
        return
    instance.slug = instance.slug or slugify(getattr(instance, instance.__slugcolumn__))
    model = instance.__class__
    with db.session.no_autoflush:
        obj = db.session.query(model).filter_by(slug=instance.slug).one_or_none()
        while obj:
            slug_elements = obj.slug.split('-')
            index = slug_elements[-1]
            try:
                index = int(index)
                slug_elements.pop(-1)
            except ValueError:
                index = 0
            instance.slug = '-'.join(slug_elements + [str(index+1)])
            obj = db.session.query(model).filter_by(slug=instance.slug).one_or_none()

def set_slug(instance):
    instance.slug = instance.slug or slugify(getattr(instance, instance.__slugcolumn__))

def populate_site_settings(instance):
    settings = Settings()
    for option in DEFAULT_SETTINGS:
        setting = Setting(key=option.name)
        setting.value = option.default
        settings.children[option.name] = setting
    instance.settings = settings

def associate_profile(instance):
    instance.profile = Profile(first_name='Your First Name', last_name='Your Last Name', bio="A Summary about you.")

def set_metadata(instance):
    if not instance.meta_title and hasattr(instance, 'title'):
        instance.meta_title = instance.title
    if not instance.meta_description:
        if instance.has_auto_desc:
            content = getattr(instance, 'content', '') or getattr(instance, 'body', '')
            instance.meta_description = make_summary(content)
    if not instance.keywords:
        instance.keywords = ','.join(getattr(instance, 'meta_title', '').split())
