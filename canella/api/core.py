from marshmallow import fields
from . import CanellaModelSchema
from . import CanellaResource
from ..core import Site, Displayable

class SiteSchema(CanellaModelSchema):
    class Meta:
        model = Site


class SiteResource(CanellaResource):
    schema = SiteSchema

class DisplayableSchema(CanellaModelSchema):
    site = fields.Nested(SiteSchema, only=['id', 'name', 'is_active'])


class DisplayableResource(CanellaResource):
    schema = None
    
    def query_one(self, pk):
        return self.schema.Meta.model.query.get(pk)
    
    def query_all(self):
        return self.schema.Meta.model.query.published

