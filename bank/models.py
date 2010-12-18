# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from django import forms
from django.utils.translation import ungettext_lazy as _


class Link(models.Model):
    href = models.URLField(_("Url"), verify_exists=False, max_length=255)
    owner = models.ForeignKey(User, verbose_name=_("Owner"))
    added = models.DateTimeField(_("Added"), auto_now_add=True)
    title = models.TextField(_("Tag title content"), blank=True, default="")
    last_check = models.DateTimeField(_("Last check"),
                                      blank=True,
                                      null=True,
                                      default=None)


class LinkAddForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ( "href", )

