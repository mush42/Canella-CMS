from flask import send_from_directory
from ..wrappers import CanellaModule
from .models import *


files = CanellaModule(
    'files', __name__)

@files.route('/media/<path:filename>', endpoint='media')
def serve_media(filename):
    return send_from_directory(app.config['MEDIA_PATH'], filename)
