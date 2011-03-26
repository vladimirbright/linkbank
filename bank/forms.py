# -*- coding: utf-8 -*-

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms.util import ErrorDict
from django import forms
from django.template.defaultfilters import escape
from django.utils.translation import ugettext_lazy as _

from captcha.fields import CaptchaField

from bank.models import Link
from tags.models import Tag


class LinkForm(forms.ModelForm):
    add_tags = forms.CharField(
                   label=_("Tags"),
                   required=False,
                   help_text=_("Enter comma separated tags")
               )

    def __init__(self, *args, **kwargs):
        super(LinkForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["add_tags"].initial = u", ".join(
                    map(escape, [ t.title for t in self.instance.tags.all() ])
                )

    def add_tags_to_link(self, user, clear=False):
        _tags = self.cleaned_data.get("add_tags", "")
        if _tags.strip():
            _tags = [ i.strip() for i in _tags.strip().split(",") ]
            if clear:
                self.instance.tags.clear()
            for t in _tags:
                tag, c = Tag.objects.get_or_create(owner=user, title=t)
                self.instance.tags.add(tag)
            self.instance.save()

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


SORT_ATTRS = (
    ("added", _("Added")),
    ("@weight", _("Relevance")),
)

class SearchForm(forms.Form):
    q = forms.CharField(required=False)
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
