# -*- coding: utf-8 -*-

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _

from captcha.fields import CaptchaField

from bank.models import Link


class LinkForm(forms.ModelForm):
    return_me_to_link = forms.BooleanField(
                            label=_("Return me to link after save"),
                            required=False
                        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        assert isinstance(self.user, User)
        super(LinkForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.instance.owner = self.user
        return super(LinkForm, self).save(*args, **kwargs)

    class Meta:
        model = Link
        fields = (
           "href",
           "title",
           "description"
        )
        widgets = {
            "title": forms.TextInput(attrs={ "class": "text" }),
            "href": forms.TextInput(attrs={ "class": "text" }),
            "description": forms.Textarea(attrs={ "class": "textarea" }),
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


