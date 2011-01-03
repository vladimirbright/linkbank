# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _


from bank.models import LinkAddForm, Link, UserCreationFormWithCaptcha, LinkEditForm
from bank.models import LinkEditForm
from tags.models import Tag


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
        # TODO send email to user about registration
        return HttpResponseRedirect('/')
    c = {}
    c["registration_form"] = form
    return render_to_response("registration/form.html", c,
                              context_instance=RequestContext(request))


def link_list(request):
    if request.user.is_anonymous():
        c = {}
        c["registration_form"] = UserCreationFormWithCaptcha()
        return render_to_response("registration/form.html", c,
                                  context_instance=RequestContext(request))
    links = Link.objects.filter(owner=request.user).order_by('-pk')
    #messages.error(request, "FUUUUUUUUUU")
    #messages.warning(request, "Maybe FUUUUUUUUU")
    #messages.success(request, "Not FUUUUUUUUU")
    #messages.info(request, "Yap, info")
    c = {}
    c["form"] = LinkAddForm(request.GET or None)
    c["links"] = links
    return render_to_response("bank/list.html", c,
                              context_instance=RequestContext(request))


@login_required
def link_delete(request, l_id):
    # TODO нормальную HTML форму для зашедших по ссылке
    if request.method != "POST" or request.is_ajax() is False:
        messages.error(request,
                       _("Deleting bookmarks by permalinks is disabled"))
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
    try:
        link = Link.objects.get(pk=l_id, owner=request.user)
    except Link.DoesNotExist:
        messages.error(request, _("Bookmark doesn't exist or not yours"))
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
    link.delete()
    return HttpResponse(u"%s" % _("Bookmark deleted"))


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
        _link = form.save(commit=False)
        _tags = form.cleaned_data.get("add_tags", "")
        if _tags.strip():
            _tags = [ i.strip() for i in _tags.strip().split(",") ]
            _link.tags.clear()
            for t in _tags:
                tag, c = Tag.objects.get_or_create(owner=request.user, title=t)
                _link.tags.add(tag)
        _link.save()
        return HttpResponse(u"%s" % _("Changes saved"))
    c = {}
    c["link"] = link
    c["form"] = form
    return render_to_response("bank/link_edit.html", c,
                              context_instance=RequestContext(request))


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
    return render_to_response("bank/error.html", c,
                              context_instance=RequestContext(request))

