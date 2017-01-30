from marshmallow import fields
from . import CanellaModelSchema
from . import CanellaResource
from ..user.models import User, Profile, Role

class ProfileSchema(CanellaModelSchema):
    user = fields.Nested('UserSchema', only=['id', 'user_name'])
    class Meta:
        model = Profile

class RoleSchema(CanellaModelSchema):
    class Meta:
        model = Role

class UserSchema(CanellaModelSchema):
    profile = fields.Nested(ProfileSchema, exclude=['user'])
    roles = fields.Nested(RoleSchema, many=True, only=['id', 'name'])
    dump_options = {
        'one': {
            'exclude': ['password', 'posts']
        },
        'many' : {
            'exclude': ['password', 'posts']
        }
    }
    class Meta:
        model = User

class ProfileResource(CanellaResource):
    schema = ProfileSchema

class UserResource(CanellaResource):
    schema = UserSchema
