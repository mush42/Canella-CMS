import os
from sqlalchemy import event, inspect
from datetime import datetime
from . import app, db
from .core.models import Site, Slugged, UniquelySlugged, Metadata, TimeStampped
from .page.models import PageBase
from .form.models import Form, Field, FieldEntry, FormEntry
from .blog.models import Tag
from .settings.models import Setting, Settings
from .user.models import User
from .util.events import (
    select_instances_of_type, change_slug_path,
    set_slug_path, ensure_singlten_is_active,
    set_unique_slug, set_slug,
    populate_site_settings, associate_profile, set_metadata
)


event_registry = {
    'before_flush': {
        Slugged: {
            'dirty': {
                'slug': set_slug
            },
            'new': {
                'slug': set_slug
            }
        },
        UniquelySlugged: {
            'dirty': {
                'slug': set_unique_slug
            },
            'new': {
                'slug': set_unique_slug
            }
        },
        Metadata: {
            'new': {
                'keywords': set_metadata
            }
        },
        PageBase: {
            'dirty': {
                'slug': set_slug_path,
                'parent_id': set_slug_path
            },
            'new': {
                'slug': set_slug_path
            }
        },
        Site: {
            'dirty': {
                'is_active': ensure_singlten_is_active
            },
            'new': {
                'is_active': ensure_singlten_is_active
            }
        },
    },
    'after_flush': {
        Site: {
            'new': {
                'settings': populate_site_settings,
            }
        },
        User: {
            'new': {
                'profile': associate_profile,
            }
        }
    }
}


@event.listens_for(db.Session, 'after_flush')
def receive_after_flush(session, flush_context):
    process_flush_event(event_registry['after_flush'], session)

@event.listens_for(db.Session, 'before_flush')
def receive_before_flush(session, flush_context, instances):
    process_flush_event(event_registry['before_flush'], session)

def process_flush_event(event_opts, session):
    for model, options in event_opts.items():
        for identity_set_name, attr_callbacks in options.items():
            instances = getattr(session, identity_set_name)
            for instance in select_instances_of_type(model, instances):
                state = inspect(instance)
                for attr, callback in attr_callbacks.items():
                    if identity_set_name == 'dirty' and attr in state.unmodified:
                        continue
                    callback(instance)


@event.listens_for(TimeStampped, 'before_update', propagate=True)
def timestampped_before_update(mapper, connection, target):
    target.updated = datetime.utcnow()

# Forms

@event.listens_for(Field, 'after_delete')
def clean_deleted_fields_files(mapper, connection, target):
    if target.type == 'file_input':
        for entry in target.entries:
                os.remove(os.path.join(app.config['FORM_UPLOADS_PATH'], entry.value))

@event.listens_for(Form, 'after_delete')
def clean_up_afterwords(mapper, connection, target):
    for field in target.fields:
        clean_deleted_fields_files(mapper=None, connection=None, target=field)
