# -*- coding: utf-8 -*-

import sphinxapi

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from bank.models import LinkAddForm, Link, UserCreationFormWithCaptcha, LinkEditForm
from bank.models import LinkEditForm
from bank.forms import SearchForm
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


PER_PAGE = getattr(settings, "LINKS_PER_PAGE", 20)


def link_list(request):
    if request.user.is_anonymous():
        c = {}
        c["registration_form"] = UserCreationFormWithCaptcha()
        return render_to_response("registration/form.html", c,
                                  context_instance=RequestContext(request))
    links = Link.objects.filter(owner=request.user).order_by('-pk')
    c = {}
    c["PER_PAGE"] = PER_PAGE
    c["form"] = LinkAddForm(request.GET or None)
    c["links"] = links
    return render_to_response("bank/list.html", c,
                              context_instance=RequestContext(request))



@login_required
def link_search(request):
    f = SearchForm(request.GET or None, user=request.user)
    f.is_valid()
    q = f.cleaned_data.get("q", "")
    s = f.cleaned_data.get("s", None)
    tags = f.cleaned_data.get("tags", None)
    _s = Link.search.sphinx
    _s.SetFilter("owner_id", [ request.user.pk, ])
    _s.SetMatchMode(sphinxapi.SPH_MATCH_EXTENDED2)
    if s:
        _s.SetSortMode(sphinxapi.SPH_SORT_ATTR_DESC, s)
    _tag_titles = []
    if tags:
        _tag_titles = [ u"%sQ%s" %(_s.EscapeString(i.title), i.pk) \
                                                                for i in tags ]
    # Take care about pagination
    try:
        _page = int(request.GET.get("page", 0))
    except ValueError:
        _page = 1
    if _page <= 0:
        _page = 1
    _offset = (_page - 1) * PER_PAGE
    _limit = _page * PER_PAGE
    _s.SetLimits(_offset, _limit, _offset + 100)
    # Take care about search query
    query = u""
    if q.strip() != "":
        query = u"@(href, title, description) %s*" % _s.EscapeString(q.strip())
    if _tag_titles:
        query += u"@tags_cache %s" % u" | ".join(_tag_titles)
    #print query
    c = {}
    c["PER_PAGE"] = PER_PAGE
    c["links"] = Link.search.query(query)
    c["fake_qs"] = range(Link.search.total_found)
    c["paginate_fake"] = True
    return render_to_response("bank/_list_ajax.html", c,
                              context_instance=RequestContext(request))


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
        return HttpResponse(_("Bookmark deleted").format())
    c = { "link": link }
    return render_to_response("bank/delete.html", c,
                              context_instance=RequestContext(request))


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
        return HttpResponse(_("Changes saved").format())
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

