from flask import url_for, jsonify
from flask_security import current_user
from jinja2 import nodes
from jinja2.ext import Extension
from wtforms.widgets.core import html_params
from urllib.parse import urlencode
from .. import app, db
from .misc import prettify_date

import random
import json
import sqlalchemy as sa

TYPE_MAP = {
    sa.types.UnicodeText: 'textarea',
    sa.types.BigInteger: 'number',
    sa.types.SmallInteger: 'number',
    sa.types.Text: 'textarea',
    sa.types.Date: 'date',
    sa.types.DateTime: 'datetime',
    sa.types.Enum: 'select',
    sa.types.Float: 'number',
    sa.types.Integer: 'number',
    sa.types.Numeric: 'number',
    sa.types.Boolean: 'checklist',
    sa.types.Unicode: 'text',
    sa.types.String: 'text',
    sa.types.Time: 'datetime',
}

@app.template_filter()
def pretty_date(date):
    return prettify_date(date)

@app.template_filter()
def args(url, qs):
    return '{}?'.format(url) + urlencode(qs)


def should_enable_inline_editing():
    rv = True
    if not app.config.get('ENABLE_INLINE_EDITING'):
        rv = False
    elif not current_user.is_authenticated or not current_user.is_active or not current_user.has_role('admin'):
        rv = False
    return rv

class EditableExtension(Extension):
    tags = set(['editable'])
    
    def parse(self, parser):
        lineno = next(parser.stream).lineno
        parts = [parser.stream.expect('name').value]
        while parser.stream.current.type != 'block_end':
            parser.stream.expect('dot')
            parts.append(parser.stream.expect('name').value)
        body = parser.parse_statements(['name:endeditable'], drop_needle=True)
        call = self.call_method(
            '_editable_loader',
            [nodes.Name(parts[-2], 'load'), nodes.Const(parts[-1])])
        output_nodes = [nodes.Output([
            nodes.MarkSafe(nodes.TemplateData('<div class="editable-container">')),
            nodes.MarkSafe(nodes.TemplateData('<div class="editable-content">'))])
        ]
        output_nodes.extend(body)
        output_nodes.extend([
            nodes.Output([nodes.MarkSafe(nodes.TemplateData('</div>'))]),
            nodes.Output([nodes.MarkSafe(call)]),
            nodes.Output([nodes.MarkSafe(nodes.TemplateData('</div>'))])
        ])
        block_name = '%s_%s_%d' %(parts[-2], parts[-1], random.randint(0, 500))
        return nodes.Block(block_name, output_nodes, True)

    def _editable_loader(self, model, attr):
        if not should_enable_inline_editing():
            return ''
        assert hasattr(model, '_sa_class_manager'), '%s is not a sqlalchemy mapped class' %model
        if not hasattr(model, attr):
            raise AttributeError('Model %s has no attribute %s' %(model, attr))
        field_data = self.widget_for(getattr(model.__class__, attr))
        titled_attr = attr.replace('_', ' ').title()
        params = dict(
            class_='editable-trigger',
            data_type=field_data['type'],
            data_pk=model.id,
            data_name=attr,
            data_url=self.api_url_for(model),
            data_title=titled_attr,
            data_value=json.dumps(getattr(model, attr)).strip('"')
        )
        if field_data['type'] == 'select':
            params['data-source'] = json.dumps(field_data['choices'])
        elif field_data['type'] == 'checklist':
            params['data-source'] = json.dumps([dict(value=json.dumps(getattr(model, attr)), text=titled_attr)])
        attrs = html_params(**params)
        return ''.join(line.lstrip() for line in """
            <a href="#" {0} role="button">
                <span class="fa-stack">
                    <i class="fa fa-circle fa-stack-2x"></i>
                    <i class="fa fa-pencil  fa-stack-1x fa-inverse"></i>
                </span>
                <span class="sr-only">Edit {1}</span>
            </a>
            """.format(attrs, titled_attr).splitlines())

    def widget_for(self, column):
        rv = dict()
        if  column.type not in TYPE_MAP and isinstance(column.type, sa.types.TypeDecorator):
            check_type = column.type.impl
        else:
            check_type = column.type
        rv['type'] = TYPE_MAP[type(check_type)]
        if column.info.get('markup'):
            rv['type'] = 'mce'
        choices = column.info.get('choices', [])
        if choices:
            rv['choices'] = [{k:str(v)} for k, v in choices]
        return rv

    def api_url_for(self, model):
        name = model.__class__.__name__.lower()
        return url_for('canella-api.%s-item' %name, pk=model.id)

app.jinja_env.extensions['canella.util.templating.EditableExtension'] = EditableExtension(app.jinja_env)