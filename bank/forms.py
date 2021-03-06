# -*- coding: utf-8 -*-

from codecs import lookup


from captcha.fields import CaptchaField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms.models import modelformset_factory
from django import forms
from django.utils.translation import ugettext_lazy as _


from bank.models import Link, Profile, ImportTask, ExportTask


LinkDeleteFormSet = modelformset_factory(Link, fields=(), can_delete=True, extra=0)


class ExportBookmarksForm(forms.ModelForm):
    hid = forms.BooleanField(initial=True, widget=forms.HiddenInput)
    class Meta:
        model = ExportTask
        fields = ()


class ImportBookmarksForm(forms.ModelForm):
    """ Form to upload file with bookmarks
    """
    class Meta:
        model = ImportTask
        fields = (
            "from_source",
            "file"
        )


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            "show_qr",
            "per_page"
        )


class LinkForm(forms.ModelForm):

    DEFAULT_LINK_ENCODING = 'utf8'

    return_me_to_link = forms.BooleanField(label=_("Return me to link after save"),
                                           required=False)
    encoding = forms.CharField(required=False,
                               initial=DEFAULT_LINK_ENCODING,
                               widget=forms.HiddenInput)

    @classmethod
    def check_encoding(cls, request):
        enc = request.REQUEST.get('encoding', '').strip()
        if enc:
            try:
                lookup(enc)
            except LookupError:
                enc = LinkForm.DEFAULT_LINK_ENCODING
        else:
            enc = LinkForm.DEFAULT_LINK_ENCODING
        request.encoding = enc
        return request

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
    captcha = CaptchaField(label=_("Type symbols"), error_messages=_errors)

    def clean_email(self):
        em = self.cleaned_data.get("email", "")
        try:
            User.objects.get(email=em)
        except User.DoesNotExist:
            return em
        _er = _("User with this email already exist")
        raise ValidationError(_er)


