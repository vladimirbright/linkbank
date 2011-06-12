# -*- coding: utf-8 -*-
import re

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext_lazy as _

from bank.forms import UserCreationFormWithCaptcha, LinkForm
from bank.models import LinkAddForm, Link, LinkEditForm


def login_or_register(request):
    c = {
        "registration_form" : UserCreationFormWithCaptcha(),
        "login_form" : AuthenticationForm(),
    }
    return render(request, "login_or_register.html", c)


def user_create(request):
    """ Registration handler """
    if request.user.is_anonymous() is False:
        return HttpResponseRedirect('/')
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


PER_PAGE = getattr(settings, "LINKS_PER_PAGE", 20)


def link_list(request):
    if request.user.is_anonymous():
        return login_or_register(request)
    links = Link.objects.filter(owner=request.user).order_by('-pk')
    c = {}
    c["PER_PAGE"] = PER_PAGE
    c["form"] = LinkAddForm(request.GET or None)
    c["links"] = links
    return render(request, "bank/list.html", c)


SEARCH_REPLACE_PATTERN = re.compile(r'[^\w\d#]', re.I + re.U)

@login_required
def link_search(request):
    q = request.GET.get("q", "").strip()
    if not q:
        links = Link.objects.filter(owner=request.user).order_by('-pk')
        djapian_use = False
    else:
        # Произошел поиск
        djapian_use = True
        links = Link.indexer.search(q).filter(owner=request.user).flags(
                    Link.indexer.flags.PARTIAL
                )
    c = {}
    c["PER_PAGE"] = PER_PAGE
    c["links"] = links
    c["query"] = q
    c["djapian_use"] = djapian_use
    return render(request, "bank/_list_ajax.html", c)


@login_required
def link_delete(request, l_id):
    # TODO нормальную HTML форму для зашедших по ссылке
    if request.is_ajax() is False:
        messages.error(request,
                       _("Deleting bookmarks by permalinks is disabled"))
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
    link = get_object_or_404(Link, pk=l_id, owner=request.user)
    if request.method == "POST" and \
       u"%s" % request.POST.get("vaaa", 0) == u"%s" % link.pk :
        link.delete()
        return render(request, "ok.html")
    c = { "link": link }
    return render(request, "bank/delete.html", c)


@login_required
def link_edit(request, l_id):
    # TODO нормальную HTML форму для зашедших по ссылке
    if request.is_ajax() is False:
        messages.error(request, _("Only via ajax"))
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
    try:
        link = Link.objects.get(pk=l_id, owner=request.user)
    except Link.DoesNotExist:
        messages.error(request, _("Bookmark doesn't exist or not yours"))
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
    form = LinkEditForm(request.POST or None, instance=link)
    if form.is_valid():
        form.save()
        return render(request, "ok.html")
    c = {}
    c["link"] = link
    c["form"] = form
    return render(request, "bank/link_edit.html", c)


@login_required
def link_create_extended(request):
    form = LinkForm(request.POST or None)
    success = False
    allready_in = False
    if form.is_valid():
        success = True
        link = form.save(commit=False)
        if not Link.objects.filter(owner=request.user,href=link.href).exists():
            link.owner = request.user
            link.save()
            form.add_tags_to_link(request.user, clear=False)
        else:
            allready_in = True
    c = {
        "form": form,
        "success": success,
        "allready_in": allready_in,
    }
    return render(request, "bank/link_create_extended.html", c)


@login_required
def link_create(request):
    form = LinkAddForm(request.GET or None)
    if form.is_valid():
        link = form.save(commit=False)
        link.owner = request.user
        if not Link.objects.filter(owner=request.user,
                                   href=link.href).exists():
            link.save()
        return HttpResponseRedirect(link.href)
    c = {}
    c["form"] = form
    if form.errors:
        messages.error(request,
                       _("FUUUUUUUU, insert correct url with http://"))
    return render(request, "bank/error.html", c)

