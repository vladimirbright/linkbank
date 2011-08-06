# -*- coding: utf-8 -*-

import re

from django.contrib.auth.models import User
from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _


DOMAIN_PATTERN = re.compile(r'https?://([^/]+)')

class Link(models.Model):
    href = models.URLField(_("Url"), verify_exists=False, max_length=255)
    owner = models.ForeignKey(User, verbose_name=_("Owner"))
    added = models.DateTimeField(_("Added"), auto_now_add=True)
    title = models.TextField(_("Title"), blank=True, default="")
    description = models.TextField(_("Description"), blank=True, default="", help_text=_("Hash tag allowed"))

    def domain(self):
        if not self.href:
            return u""
        res = DOMAIN_PATTERN.match(self.href)
        if not res:
            return u""
        return res.groups()[0]


def djapian_update(sender, **kwargs):
    Link.indexer.update()
models.signals.post_save.connect(
    djapian_update,
    sender=Link,
    dispatch_uid="link.djapian_update"
)


def djapian_delete(sender, instance, **kwargs):
    Link.indexer.delete(instance)
models.signals.pre_delete.connect(
    djapian_delete,
    sender=Link,
    dispatch_uid="link.djapian_delete"
)



class LinkAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LinkAddForm, self).__init__(*args, **kwargs)
        self.fields["href"].initial = _("Add link")

    class Meta:
        model = Link
        fields = ( "href", "title", "description" )


class LinkEditForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ( "href", "title", "description", )
        widgets = {
            "title": forms.TextInput
        }
