from flask import g
from werkzeug.routing import PathConverter
from flask import  render_template, abort
from .slugging import clean_slashes


class PathToSlugConvertor(PathConverter):

    def to_python(self, value):
        return clean_slashes(value)

    def to_url(self, value):
        return '/{}/'.format(value)

def templates_for_page(page):
    if page.is_home:
        return 'site/index.html'
    slug = page.slug_path
    templates = ["page", page.__contenttype__] + slug.split('/')
    templates.reverse()
    print(templates)
    return ['site/page/{}.html'.format(t) for t in templates]

def render_page_template(page=None, context=None, template=None):
    page = g.page
    context = context or dict()
    context.setdefault('page', page)
    if not template:
        template = templates_for_page(page)
    return render_template(template, **context)