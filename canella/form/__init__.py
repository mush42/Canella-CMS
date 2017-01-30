import time
import os.path
from flask import request, make_response, redirect, g, render_template, url_for, abort, flash
from werkzeug import secure_filename
from flask_wtf import Form as HtmlForm
from ..page import page
from .. import app, db
from ..util.dynamicform import DynamicForm
from ..util.misc import date_stamp
from .models import FormEntry, FieldEntry, Form, Field


def store_form(form):
    entry = FormEntry(form_id=g.page.id)
    for f in form:
        field = Field.query.filter_by(form_id=g.page.id).filter_by(name=f.name).one_or_none()
        if field is None:
            continue
        field_entry = FieldEntry(field_id=field.id)
        data = f.data
        if field.type == 'file_input':
            file_data = request.files[field.name]
            filename = '%s-%s-%s.%s' %(field.name, date_stamp(), str(time.time()).replace('.', ''), os.path.splitext(file_data.filename)[-1])
            path = os.path.join(app.config['FORM_UPLOADS_PATH'], secure_filename(filename))
            file_data.save(path)
            data = filename
        field_entry.value = data
        db.session.add(field_entry)
        entry.fields.append(field_entry)
    db.session.add(entry)
    db.session.commit()


@page.handler('form', methods=['GET', 'POST'])
def form_view():
    form = DynamicForm(*g.page.fields).form
    if form.validate_on_submit():
        store_form(form)
        return redirect(request.path + '?submited=1')
    return dict(form=form)
    
