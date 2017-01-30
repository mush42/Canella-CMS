from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.ext.associationproxy import association_proxy
from flask_security import UserMixin, RoleMixin
from sqlalchemy.ext.associationproxy import association_proxy
from .. import db
from ..babel import lazy_gettext
from ..core.models import UniquelySlugged, TimeStampped
from ..files.models import ImageMixin
from ..util.sqla import PolymorphicVerticalProperty, ProxiedDictMixin

roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True,
        info=dict(label=lazy_gettext('Name'), description=lazy_gettext('A name to identify this role'))
    )
    description = db.Column(db.Unicode(255),
        info=dict(label=lazy_gettext('Description'), description=lazy_gettext('A simple summary about this role.'))
    )

    def __str__(self):
        return self.name

class User(db.Model, UserMixin, UniquelySlugged):
    __slugcolumn__ = 'user_name'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.Unicode(128), nullable=False, unique=True, index=True,
        info=dict(label=lazy_gettext('User Name'), description=lazy_gettext('A unique name for this user (used for login)'))
    )
    email = db.Column(db.String(255), unique=True,
        info=dict(label=lazy_gettext('Email'), description=lazy_gettext(''))
    )
    password = db.Column(db.String(255),
        info=dict(label=lazy_gettext('Password'), description=lazy_gettext(''))
    )
    active = db.Column(db.Boolean,
        info=dict(label=lazy_gettext('Active'), description=lazy_gettext('Activate or deactivate this user account'))
    )
    confirmed_at = db.Column(db.DateTime(),
        info=dict(label=lazy_gettext('Confirmed At'))
    )
    profile = db.relationship("Profile", backref="user", uselist=False, cascade="delete, delete-orphan",
        info=dict(label=lazy_gettext('Profile'), description=lazy_gettext(''))
    )
    roles = db.relationship('Role', secondary=roles_users,
        backref=db.backref('users', lazy='dynamic'),
        info=dict(label=lazy_gettext('Roles'), description=lazy_gettext(''))
    )
    
    name = property(fget=lambda self: self.profile.name)

    def __str__(self):
        return self.user_name

    def __repr__(self):
        return 'User(user_name={})'.format(self.user_name)

class Profile(ProxiedDictMixin, db.Model, TimeStampped, ImageMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False,
        info=dict(label=lazy_gettext('User'))
    )
    extras = db.relationship("ProfileExtras", collection_class=attribute_mapped_collection('key'))
    _proxied = association_proxy("extras", "value")
    first_name = db.Column(db.Unicode(255), nullable=False,
        info=dict(label=lazy_gettext('First Name'), description=lazy_gettext(''))
    )
    last_name = db.Column(db.Unicode(255), nullable=False,
        info=dict(label=lazy_gettext('Last Name'), description=lazy_gettext(''))
    )
    bio = db.Column(db.Text,
        info=dict(label=lazy_gettext('Biography'), description=lazy_gettext(''))
    )

    @property
    def name(self):
        return ' '.join([self.first_name, self.last_name])

    @name.setter
    def name(self, value):
        self.first_name, self.last_name = value

    def __str__(self):
        return "{}'s Profile".format(self.name)

    def __repr__(self):
        return 'Profile(user={})'.format(self.name)

class ProfileExtras(PolymorphicVerticalProperty, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))
    key = db.Column(db.String(128))
    type = db.Column(db.String(64))
    int_value = db.Column(db.Integer, info={'type': (int, 'integer')})
    str_value = db.Column(db.Unicode(255), info={'type': (str, 'string')})
    bool_value = db.Column(db.Boolean, info={'type': (bool, 'boolean')})
