from sqlalchemy.ext.hybrid import hybrid_property
from .. import app, db
from ..babel import lazy_gettext
from ..core.models import TimeStampped
from ..page.models import Page
from ..util.dynamicform import FIELD_MAP
from ..util.sqla import PolymorphicVerticalProperty



class Field(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False,
        info=dict(label=lazy_gettext('Field Name'), description=lazy_gettext('Should contain only letters, numbers, and under scors, and should not start with a number'))
    )
    label = db.Column(db.Unicode(255), nullable=False,
        info=dict(label=lazy_gettext('Field Label'), description=lazy_gettext('The input label'))
    )
    description = db.Column(db.Unicode(255),
        info=dict(label=lazy_gettext('Field Description'), description=lazy_gettext('A summary about the field'))
    )
    type = db.Column(db.Enum(*FIELD_MAP.keys()), nullable=False,
        info=dict(choices=[(k, v.name) for k, v in FIELD_MAP.items()], label=lazy_gettext('Field Type'), description=lazy_gettext('HTML Type of the field'))
    )
    choices = db.Column(db.Unicode,
        info=dict(label=lazy_gettext('Field Choices'), description=lazy_gettext('If it is a select'))
    )
    default = db.Column(db.Unicode,
        info=dict(label=lazy_gettext('Default Value'), description=lazy_gettext('Default value to populate the field'))
    )
    required = db.Column(db.Boolean, default=False,
        info=dict(label=lazy_gettext('Required'), description=lazy_gettext('Whether this field is required or not'))
    )
    max_length = db.Column(db.Integer, default=255,
        info=dict(label=lazy_gettext('Maximom Length'), description=lazy_gettext('Max number of chars the user can enter'))
    )
    form_id = db.Column(db.Integer, db.ForeignKey('form.id'))

class Form(Page):
    __contenttype__ = 'form'
    id = db.Column(db.Integer, db.ForeignKey('page.id'), primary_key=True)
    submit_text = db.Column(db.String(255),
        info=dict(label=lazy_gettext('Submit button text'), description=lazy_gettext('Text of the submit button in the form'))
    )
    submit_message = db.Column(db.UnicodeText,
        info=dict(label=lazy_gettext('After Submit Message'), description=lazy_gettext('A Message to display for the user after submitting the form'))
    )
    fields = db.relationship(Field, backref='form')

class FormEntry(TimeStampped, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    form_id = db.Column(db.Integer, db.ForeignKey('form.id'))
    form = db.relationship('Form', backref='entries')

class FieldEntry(db.Model, PolymorphicVerticalProperty):
    id = db.Column(db.Integer, primary_key=True)
    entry_id = db.Column(db.Integer, db.ForeignKey(FormEntry.id))
    entry = db.relationship('FormEntry', backref='fields')
    field_id = db.Column(db.Integer, db.ForeignKey('field.id'))
    field = db.relationship('Field', backref='entries')
    type = db.Column(db.String(64))
    int_value = db.Column(db.Integer, info=dict(type=(int, 'integer')))
    str_value = db.Column(db.UnicodeText, info=dict(type=(str, 'string')))
    bool_value = db.Column(db.Boolean, info=dict(type=(bool, 'boolean')))
