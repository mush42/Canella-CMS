from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.ext.associationproxy import association_proxy
from ..util.sqla import PolymorphicVerticalProperty, ProxiedDictMixin
from .. import db


class Setting(PolymorphicVerticalProperty, db.Model):
    __tablename__ = 'setting'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('settings.id'))
    key = db.Column(db.String(128))
    type = db.Column(db.String(64))
    int_value = db.Column(db.Integer, info={'type': (int, 'integer')})
    str_value = db.Column(db.Unicode(255), info={'type': (str, 'string')})
    bool_value = db.Column(db.Boolean, info={'type': (bool, 'boolean')})

    def __repr__(self):
        return '<Setting key={}>'.format(self.key)

class Settings(ProxiedDictMixin, db.Model):
    id =  db.Column(db.Integer, primary_key=True)
    children = db.relationship("Setting", collection_class=attribute_mapped_collection('key'))
    _proxied = association_proxy("children", "value")
    site_id = db.Column(db.Integer, db.ForeignKey('site.id'), nullable=False)
