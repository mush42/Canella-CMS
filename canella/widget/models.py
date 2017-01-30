from .. import db
from . import WidgetWidth, WidgetLocation

class WidgetGard(db.Model):
    widgets = dict()
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(255))
    name = db.Column(db.String(255))
    width = db.Column(db.Enum(WidgetWidth))
    location = db.Column(db.Enum(WidgetLocation))

    @classmethod
    def register_widget(cls, widget, path):
        new = cls(name=widget.name, path=path, width=widget.width, location=widget.location)
        db.session.add(new)
        db.session.commit()
        self.widgets[widget.name] = widget
        