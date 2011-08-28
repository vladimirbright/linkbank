# -*- coding: utf-8 -*-

import re

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Profile(models.Model):
    user = models.OneToOneField(User)
    show_qr = models.BooleanField(_("Show QR codes"), default=True)
    _per_page_choices = [ (i,i) for i in range(10,51,10) ]
    per_page = models.IntegerField(_("Links per page"), choices=_per_page_choices, default=20)

    def __unicode__(self):
        return u"Profile for user # %s" %self.user_id

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")


def create_profile(sender, instance, created, **kwargs):
    """
        Create Profile on User create
    """
    if created:
        Profile.objects.get_or_create(user=instance)
models.signals.post_save.connect(
    create_profile,
    sender=User,
    dispatch_uid="bank.create_profile"
)


DOMAIN_PATTERN = re.compile(r'https?://([^/]+)')

class Link(models.Model):
    href = models.URLField(_("Url"), verify_exists=False, max_length=255, help_text=_("http:// or https:// required"))
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

    def __unicode__(self):
        return u"%s for user # %s" %(self.href[:30], self.owner_id)

    class Meta:
        verbose_name = _("Bookmark")
        verbose_name_plural = _("Bookmarks")


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

