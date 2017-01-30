from marshmallow import fields
from . import CanellaModelSchema
from . import CanellaResource
from ..settings.models import Setting, Settings


class SettingSchema(CanellaModelSchema):
    class Meta:
        model = Setting

class SettingsSchema(CanellaModelSchema):
    children = fields.Nested(SettingSchema, many=True, only=['key', 'value'])
    class Meta:
        model = Settings

class SettingsResource(CanellaResource):
    schema = SettingsSchema
    
