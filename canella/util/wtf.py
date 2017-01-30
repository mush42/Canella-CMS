from flask import url_for, render_template
from wtforms import StringField, TextAreaField
from wtforms.widgets import TextArea, TextInput
from ..babel import lazy_gettext

class RichTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' mceEditor'
        else:
            kwargs.setdefault('class', 'mceEditor')
        return super(RichTextAreaWidget, self).__call__(field, **kwargs)

class RichTextAreaField(TextAreaField):
        widget = RichTextAreaWidget()

class FileSelectorInput(TextInput):
    def __init__(self, field=None, render_args=None, **kw):
        self.html_class = kw.pop('class', '')
        self.render_args = render_args
        super(FileSelectorInput, self).__init__(field, **kw)

    def __call__(self, field, **kwargs):
        kwargs['class'] = kwargs.get('class', '') + ' file-input'
        kwargs['data-name'] = self.render_args['name']
        html = super(FileSelectorInput, self).__call__(field, type='hidden', **kwargs)
        return html + render_template('canella/admin/widgets/file-selector.html', **self.render_args)

class FileSelectorField(StringField):
    def __init__(self, *args, render_args=None, **kwargs):
        if render_args is None:
            render_args = dict()
        self.render_args = render_args
        self.render_args.setdefault('button_text', kwargs.pop('button_text', lazy_gettext('Select A File')))
        self.render_args.setdefault('target_url', kwargs.pop('target_url', url_for('media.index')))
        super(FileSelectorField, self).__init__(*args, **kwargs)
        self.render_args.setdefault('label', kwargs.pop('label', lazy_gettext('File')))
        self.render_args.setdefault('name', self.name)
        self.widget = FileSelectorInput(render_args=self.render_args)
