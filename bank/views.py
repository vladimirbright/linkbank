# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView

from bank.forms import UserCreationFormWithCaptcha, LinkForm, ProfileEditForm
from bank.models import Link, Profile
from helpers.decorators import anonymous_required


class BookmarkletsView(TemplateView):
    """
        Bookmarklets page
    """
    template_name = "bookmarklets.html"

    def get_context_data(self):
        return {
            "nav": {
                "bookmarklets": True,
            },
        }


class LoginOrRegisterPageView(TemplateView):
    """
        Index page to anon
        Login and register form
    """
    template_name = "login_or_register.html"

    def get_context_data(self):
        return {
            "registration_form" : UserCreationFormWithCaptcha(),
            "login_form" : AuthenticationForm(),
        }


@anonymous_required
def user_create(request):
    """
        Registration page
    """
    form = UserCreationFormWithCaptcha(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        user.email = form.cleaned_data["email"]
        user.is_active = True
        user.save()
        messages.success(
            request,
            _("Registration is done. You may login as user %(username)s") % {
                "username": user.username
            }
        )
        # TODO send email to user about registration
        return HttpResponseRedirect('/')
    c = {}
    c["registration_form"] = form
    return render(request, "registration/form.html", c)


def link_list(request):
    """
        List of bookmarks
    """
    if request.user.is_anonymous():
        return LoginOrRegisterPageView.as_view()(request)
    links = Link.objects.filter(owner=request.user).order_by('-pk')
    c = {
        "links": links,
        "nav": {
            "index": True,
        },
        "PER_PAGE": Profile.objects.get_or_create(user=request.user)[0].per_page
    }
    return render(request, "index2.html", c)


@login_required
def profile_edit(request):
    """
        "Settings" page
    """
    profile = Profile.objects.get_or_create(user=request.user)[0]
    profile_form = ProfileEditForm(
                       request.POST or None,
                       instance=profile,
                       prefix="profile"
                   )
    if profile_form.is_valid():
        profile_form.save()
        messages.success(request, _("Settings saved"))
        return HttpResponseRedirect("/")
    c = {
        "profile": profile,
        "profile_form": profile_form,
        "nav": { "settings": True },
    }
    return render(request, "profile_edit.html", c)


@login_required
def link_search(request):
    """
        Ajax handler to load search
    """
    q = request.GET.get("q", "").strip()
    if q:
        links = Link.indexer.search(q).filter(owner=request.user).flags(
                    Link.indexer.flags.PARTIAL
                )
    else:
        links = Link.objects.filter(owner=request.user).order_by('-pk')
    c = {
        "links": links,
        "PER_PAGE": Profile.objects.get_or_create(user=request.user)[0].per_page
    }
    return render(request, "link_list.html", c)


@login_required
def link_delete(request, l_id):
    """
        Delete bookmark handler
    """
    # TODO нормальную HTML форму для зашедших по ссылке
    if not request.is_ajax():
        messages.error(request, _("Deleting bookmarks by permalinks is disabled"))
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
    link = get_object_or_404(Link, pk=l_id, owner=request.user)
    if request.method == "POST" and \
       u"%s" % request.POST.get("vaaa", 0) == u"%s" % link.pk :
        link.delete()
        return render(request, "ok.html")
    c = { "link": link }
    return render(request, "bank/delete.html", c)


@login_required
@transaction.commit_on_success
def link_edit(request, l_id):
    # TODO нормальную HTML форму для зашедших по ссылке
    if not request.is_ajax():
        messages.error(request, _("Only via ajax"))
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
    try:
        link = Link.objects.get(pk=l_id, owner=request.user)
    except Link.DoesNotExist:
        messages.error(request, _("Bookmark doesn't exist"))
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
    form = LinkForm(request.POST or None, instance=link, user=request.user)
    form.fields.pop("return_me_to_link", None)
    if form.is_valid():
        form.save()
        return render(request, "ok.html")
    c = {}
    c["link"] = link
    c["form"] = form
    return render(request, "bank/link_edit.html", c)


@login_required
@transaction.commit_on_success
def link_create_extended(request):
    """
        Page to add bookmark
    """
    form = LinkForm(request.POST or None, user=request.user)
    if form.is_valid():
        link = form.save()
        if form.cleaned_data.get("return_me_to_link", False):
            return HttpResponseRedirect(link.href)
        return HttpResponseRedirect(reverse("index"))
    c = {
        "form": form,
        "nav": {
            "add": True,
        }
    }
    return render(request, "link_create_extended.html", c)


@login_required
def link_create(request):
    """
        Bookmarklet handler
    """
    _get = request.GET.copy()
    _get["return_me_to_link"] = 1
    form = LinkForm(_get, user=request.user)
    if form.is_valid():
        link = form.save(commit=False)
        if not Link.objects.filter(owner=request.user, href=link.href).exists():
            link.save()
        return HttpResponseRedirect(link.href)
    c = {
        "form": form,
        "nav": {
            "add": True,
        }
    }
    return render(request, "link_create_extended.html", c)

