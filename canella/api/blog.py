from marshmallow import fields
from . import CanellaModelSchema
from . import CanellaResource
from ..blog.models import Post, Category, Tag, Comment
from ..util.blog import make_summary
from .core import DisplayableSchema, DisplayableResource
from .user import UserSchema

class CategorySchema(CanellaModelSchema):
    class Meta:
        model = Category

class TagSchema(CanellaModelSchema):
    class Meta:
        model = Tag

class CommentSchema(CanellaModelSchema):
    class Meta:
        model = Comment

class PostSchema(DisplayableSchema):
    tags = fields.Nested(TagSchema, many=True, only=['id', 'title'])
    category = fields.Nested(CategorySchema, only=['id', 'title'])
    author = fields.Nested(UserSchema, only=['id', 'user_name', 'profile.name'])
    summary = fields.Function(serialize=lambda o: make_summary(o.body))
    site_endpoint = ('canella-blog.post', {'slug': '<slug>'})
    dump_options = {
        'many': {
            'only': ['id', 'title', 'summary', 'created', 'updated', 'site_url']
        }
    }

    class Meta(DisplayableSchema.Meta):
        model = Post

class PostResource(DisplayableResource):
    schema = PostSchema

