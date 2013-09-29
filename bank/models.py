# -*- coding: utf-8 -*-

import re


from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


from helpers.validators import FileSizeValidator


HASHTAG_PATTERN = re.compile(r'#([\S]+)', re.U + re.I)


class ImportTask(models.Model):
    """ Import bookmarks tasks
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    added = models.DateTimeField(_("Added"), auto_now_add=True)
    from_source_choices = (
        ("delicious", _("delicious.com")),
        ("google", _("google.com")),
        ("custom_html", _("Custom html")),
    )
    from_source = models.CharField(
        _("Bookmarks source"),
        max_length=50,
        choices=from_source_choices
    )
    status_choices = (
        (1, _("New")),
        (2, _("In process")),
        (3, _("Success")),
        (4, _("Error")),
    )
    status = models.IntegerField(_("Status of task"), choices=status_choices, default=status_choices[0][0])
    max_size = 10 * 1024 * 1024
    file = models.FileField(_("File"), upload_to="upl/imp/%Y/%m/%d", validators=[
        FileSizeValidator(max_size=max_size),
    ])

    def __unicode__(self):
        return u"Import task bu user %s" % self.user_id

    class Meta:
        verbose_name = _("Import task")
        verbose_name_plural = _("Import tasks")


def get_export_file_path(instance, filename):
    return u"ex/%s/%s" %(instance.user_id, filename.lower())


class ExportTask(models.Model):
    """ Export bookmarks tasks
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    added = models.DateTimeField(_("Added"), auto_now_add=True)
    status_choices = (
        (1, _("New")),
        (2, _("In process")),
        (3, _("Success")),
        (4, _("Error")),
    )
    status = models.IntegerField(_("Status of task"), choices=status_choices, default=status_choices[0][0])
    file = models.FileField(_("File"), upload_to=get_export_file_path, blank=True)

    @models.permalink
    def get_absolute_url(self):
        return ("download_exported_file", [ self.pk, ])

    def __unicode__(self):
        return u"Export task bu user %s" % self.user_id

    class Meta:
        verbose_name = _("Export task")
        verbose_name_plural = _("Export tasks")


class Profile(models.Model):
    """
        User settings
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
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
    sender=settings.AUTH_USER_MODEL,
    dispatch_uid="bank.create_profile"
)


DOMAIN_PATTERN = re.compile(r'https?://([^/]+)')

class Link(models.Model):
    href = models.URLField(_("Url"), max_length=255, help_text=_("http:// or https:// required"))
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Owner"))
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
