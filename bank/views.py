# -*- coding: utf-8 -*-
from collections import defaultdict

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.db import connections, transaction

from bank.forms import SearchForm, UserCreationFormWithCaptcha
from bank.models import LinkAddForm, Link, LinkEditForm
from tags.models import Tag


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


@login_required
def link_search(request):
    f = SearchForm(request.GET or None, user=request.user)
    f.is_valid()
    _cleaned_data = getattr(f, "cleaned_data", {})
    q = _cleaned_data.get("q", "")
    s = _cleaned_data.get("s", None)
    tags = _cleaned_data.get("tags", None)
    search_pattern = u"SELECT * FROM links WHERE %(where)s ORDER BY %(order)s LIMIT %(offset)s, %(limit)s"
    search_params = defaultdict(lambda: [])
    # Take care about Link owner
    search_params["where"].append("owner_id=%s" % request.user.pk)
    # Take care about order by
    search_params["order"] = u"@id DESC"
    if s:
        search_params["order"] = u"%s DESC" % s
    # Take care about pagination
    try:
        page = int(request.GET.get("page", 0))
    except ValueError:
        page = 1
    if page <= 0:
        page = 1
    search_params["offset"] = (page - 1) * PER_PAGE
    search_params["limit"] = page * PER_PAGE
    # Take care about search query
    query = u""
    if q.strip() != "":
        query = u"@(href,title,description) %s*" % q
    # Take care about tags
    if tags:
        query += u" @tags_cache %s" % u" ".join([ u"%sQ%s" %(i.title, i.pk) for i in tags ])
    query = query.strip()
    margs = []
    if query:
        margs.append(query)
        search_params["where"].append(u"MATCH(%s)")
    search_params["where"] = u" AND ".join(search_params["where"])
    search_query = search_pattern % search_params
    with transaction.commit_manually():
        sph = connections["sphinx"].cursor()
        sph.execute(search_query, margs)
        links = [ int(i[0]) for i in sph.fetchall() ]
        sph.execute("SHOW META")
        meta = dict([ (unicode(i[0]), unicode(i[1])) for i in sph.fetchall() ])
        sph.close()
    total_found = int(meta["total_found"])
    _links = Link.objects.filter(pk__in=links)
    for i in _links:
        try:
            links[links.index(i.pk)] = i
        except IndexError:
            continue
    c = {}
    c["PER_PAGE"] = PER_PAGE
    c["links"] = links
    c["fake_qs"] = range(total_found) if total_found > 1 else [1,2,3]
    c["paginate_fake"] = True
    c["tags"] = tags
    c["query"] = q
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
        _link = form.save(commit=False)
        _tags = form.cleaned_data.get("add_tags", "")
        if _tags.strip():
            _tags = [ i.strip() for i in _tags.strip().split(",") ]
            _link.tags.clear()
            for t in _tags:
                tag, c = Tag.objects.get_or_create(owner=request.user, title=t)
                _link.tags.add(tag)
        _link.save()
        return render(request, "ok.html")
    c = {}
    c["link"] = link
    c["form"] = form
    return render(request, "bank/link_edit.html", c)


@login_required
def link_create_extended(request):
    c = {}
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

