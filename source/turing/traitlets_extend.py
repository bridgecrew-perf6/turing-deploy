# coding=utf-8

from traitlets import (
    Unicode, List,
)


class URLPrefix(Unicode):
    def validate(self, obj, value):
        u = super().validate(obj, value)
        if not u.startswith('/'):
            u = '/' + u
        if not u.endswith('/'):
            u += '/'
        return u


class Command(List):
    """Traitlet for a command that should be a list of strings,
    but allows it to be specified as a single string.
    """

    def __init__(self, default_value=None, **kwargs):
        kwargs.setdefault('minlen', 1)
        if isinstance(default_value, str):
            default_value = [default_value]
        super().__init__(Unicode, default_value, **kwargs)

    def validate(self, obj, value):
        if isinstance(value, str):
            value = [value]
        return super().validate(obj, value)
