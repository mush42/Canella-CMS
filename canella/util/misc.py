from flask import request
from werkzeug.contrib.atom import AtomFeed
from datetime import datetime
from dateutil.parser import parse
from .ext.dateformat import pretty_date

def prettify_date(s):
    date_time = s
    if isinstance(date_time, str):
        date_time = parse(s)
    return pretty_date(date_time)

def date_stamp(date=None):
    if not date:
        date = datetime.now()
    return date.strftime('%y-%m-%d__%H-%M-%S')