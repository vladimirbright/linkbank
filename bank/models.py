# -*- coding: utf-8 -*-

import re

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _

from captcha.fields import CaptchaField

from tags.models import Tag
from bank.managers import SearchManager


class UserCreationFormWithCaptcha(UserCreationForm):
    email = forms.EmailField(label=_("Email"))
    _errors = {
            "invalid": _("Wrong symbols"),
        }
    captcha = CaptchaField(label=_("Type simbols"), error_messages=_errors)

    def clean_email(self):
        em = self.cleaned_data.get("email", "")
        try:
            User.objects.get(email=em)
        except User.DoesNotExist:
            return em
        _er = _("User with this email already exist")
        raise ValidationError(_er)


DOMAIN_PATTERN = re.compile(r'https?://([^/]+)')

class Link(models.Model):
    href = models.URLField(_("Url"), verify_exists=False, max_length=255)
    owner = models.ForeignKey(User, verbose_name=_("Owner"))
    added = models.DateTimeField(_("Added"), auto_now_add=True)
    title = models.TextField(_("Title"), blank=True, default="")
    description = models.TextField(_("Description"), blank=True, default="")
    tags_cache = models.TextField(_("Tags cache"), blank=True, default="")
    tags = models.ManyToManyField(Tag,
                                  verbose_name=_("Tags"),
                                  blank=True,
                                  null=True,
                                  default=None)

    objects = models.Manager()
    search = SearchManager("links")

    def _check_tags_cache(self):
        if self.pk is None:
            return
        _cache = u""
        _titles = [ u"%sQ%s" %(t.title, t.pk) \
                                   for t in self.tags.all().order_by('title') ]
        if _titles:
            _cache = u"%s" % u"\n".join(_titles)
        self.tags_cache = _cache

    @classmethod
    def get_tag_lookup_token(cls, tag):
        if not isinstance(tag, Tag):
            raise ValueError(u"%s" % _("Tag instance required"))
        return u",%s:%s," %( tag.title, tag.pk )

    def domain(self):
        if not self.href:
            return u""
        res = DOMAIN_PATTERN.match(self.href)
        if not res:
            return u""
        return res.groups()[0]

    def save(self, *args, **kwargs):
        self._check_tags_cache()
        return super(Link, self).save(*args, **kwargs)


class LinkAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LinkAddForm, self).__init__(*args, **kwargs)
        self.fields["href"].initial = _("Add link")

    class Meta:
        model = Link
        fields = ( "href", "title", "description" )


class LinkEditForm(forms.ModelForm):
    add_tags = forms.CharField(label=_("Tags"), required=False)

    def __init__(self, *args, **kwargs):
        super(LinkEditForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields["add_tags"].initial = u", ".join([ t.title \
                                           for t in self.instance.tags.all() ])

    class Meta:
        model = Link
        fields = ( "href", "title", "description", )
        widgets = {
                "title": forms.TextInput
            }
