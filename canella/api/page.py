from marshmallow import fields
from ..page.models import Page
from .core import DisplayableSchema, DisplayableResource

class PageSchema(DisplayableSchema):
    parent = fields.Nested('self', only=['id', 'title'])
    children = fields.Nested('self', many=True, only=['id', 'title'])
    site_endpoint = ('canella-page.get_page_by_slug', {'slug': '<slug_path>'})
    dump_options = {
        'one': {
            'exclude': []
        },
        'many': {
            'only': ['id', 'title', 'content', 'created', 'updated', 'site_url']
        }
    }

    class Meta:
        model = Page

class PageResource(DisplayableResource):
    schema = PageSchema
