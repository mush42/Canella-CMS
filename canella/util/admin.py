import os.path
from werkzeug.utils import secure_filename
from datetime import datetime
from inspect import getmro
from functools import wraps
from .misc import prettify_date


def date_column_formatter(view, value):
    return prettify_date(value)


def get_aggregated_prop(cls, attr_name, res=[]):
    for base in getmro(cls):
        if base is object:
            continue
        if hasattr(base, attr_name):
            res.append(getattr(base, attr_name))
    return res



def generate_file_name(model_or_str, file_data):
    name = model_or_str
    if not isinstance(model_or_str, str):
        name = model_or_str.name
    ext = os.path.splitext(file_data.filename)[-1]
    return secure_filename('{0}-{1}{2}'.format(name, datetime.now(), ext))