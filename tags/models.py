# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Tag(models.Model):
    title = models.CharField(_("Tag"), max_length=50)
    description = models.TextField(_("Description"), blank=True, default="")
    owner = models.ForeignKey(User, verbose_name=_("Owner"))
    added = models.DateTimeField(_("Added"), auto_now_add=True)

    class Meta:
        unique_together = ("owner", "title")
