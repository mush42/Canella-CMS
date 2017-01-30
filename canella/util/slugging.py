import re
from .ext.unicode_slugify import slugify as actual_slugify

def clean_slashes(path):
    """
    Canonicalize path by removing leading slashes and trailing slashes.
    """
    return path.strip("/")

def slugify(s, **options):
    """
	Creates a slug
    """
    return actual_slugify(s, **options)

def split_slug(slug):
    slugs = slug.split('/')
    root = slugs[0]
    path = ''
    if len(slugs) >0:
        path = '/'.join(slugs[1:])
    return (root, path)
