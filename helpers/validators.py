# -*- coding: utf-8 -*-

from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _


class FileSizeValidator(object):
    """
        Validates upload file size
    """
    error_messages = {
        "too_big" : _("File is to big. Less than %(filesize)s required."),
        "too_small" : _("File is to small. More than %(filesize)s required."),
    }
    min_size = None
    max_size = None

    def __init__(self, min_size=None, max_size=None, error_messages=None):
        assert any((min_size, max_size)), "min_size or max_size required"
        if not min_size is None:
            self.min_size = int(min_size)
        if not max_size is None:
            self.max_size = int(max_size)
        if isinstance(error_messages, dict):
            self.error_messages.update(error_messages)

    def __call__(self, file_obj):
        if not self.min_size is None:
            if file_obj.size < self.min_size:
                raise ValidationError(self.error_messages["too_small"] %{ "filesize": filesizeformat(self.min_size) })
        if not self.max_size is None:
            if file_obj.size > self.max_size:
                raise ValidationError(self.error_messages["too_big"] %{ "filesize": filesizeformat(self.max_size) })

