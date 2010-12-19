# -*- coding: utf-8 -*-

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from captcha.fields import CaptchaField


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
