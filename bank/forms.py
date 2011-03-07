# -*- coding: utf-8 -*-

import sphinxapi

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms.util import ErrorDict
from django import forms
from django.utils.translation import ugettext_lazy as _

from captcha.fields import CaptchaField

from tags.models import Tag


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


MATCH_MODES = (
    (sphinxapi.SPH_MATCH_ALL, _("Match all")),
    (sphinxapi.SPH_MATCH_ANY, _("Match any")),
    (sphinxapi.SPH_MATCH_PHRASE, _("Match phrase")),
)
SORT_ATTRS = (
    ("added", _("Added")),
    ("@weight", _("Relevance")),
)

class SearchForm(forms.Form):
    q = forms.CharField(required=False)
    m = forms.ChoiceField(choices=MATCH_MODES, required=False)
    s = forms.ChoiceField(choices=SORT_ATTRS, required=False)
    tags = forms.ModelMultipleChoiceField(required=False,
                                          queryset=Tag.objects.none())
    def __init__(self, *args, **kwargs):
        _user = kwargs.pop("user")
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields["tags"].queryset = Tag.objects.filter(owner=_user)

    def full_clean(self):
        """
        Dirty hack to prevert deleting of self.cleaned_data
        """
        self._errors = ErrorDict()
        if not self.is_bound: # Stop further processing.
            return
        self.cleaned_data = {}
        if self.empty_permitted and not self.has_changed():
            return
        self._clean_fields()
        self._clean_form()
        self._post_clean()
