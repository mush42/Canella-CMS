from enum import IntEnum

class WidgetWidth(IntEnum):
    full = 1
    half = 2
    third = 3
    quarter = 4

class WidgetLocation(IntEnum):
    top = 1
    right = 2
    bottom = 3
    left = 4

class Widget(object):
    """A Widget is a snipit of html to be inserted in a page"""
    
    name = ''
    display_name = ''
    description = ''
    template = None
    """Widget template to be included"""
    static_files = dict(css=tuple(), js=tuple())
    """List of static files to be included in the page tail"""
    width = WidgetWidth.full
    location = WidgetLocation.top
    def contribute_context(self, view=None):
        """Widget specific context variables"""
        return {}
