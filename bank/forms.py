# -*- coding: utf-8 -*-

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms
from django.utils.translation import ugettext_lazy as _

from captcha.fields import CaptchaField

from bank.models import Link


class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = (
           "href",
           "title",
           "description"
        )
        widgets = {
            "title": forms.TextInput
        }


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


