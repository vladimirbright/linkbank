# -*- coding: utf-8 -*-

import logging


from datetime import datetime
from datetime import timedelta
from json import dumps


from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.db import transaction
from django.db.models import Q
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView
from django.views.generic import TemplateView


from bank.forms import ExportBookmarksForm
from bank.forms import ImportBookmarksForm
from bank.forms import LinkDeleteFormSet
from bank.forms import LinkForm
from bank.forms import ProfileEditForm
from bank.forms import UserCreationFormWithCaptcha
from bank.models import ExportTask
from bank.models import ImportTask
from bank.models import Link
from bank.models import Profile
from helpers.decorators import anonymous_required


logger = logging.getLogger(__name__)


@login_required
def download_exported_file(request, task_id):
    task = get_object_or_404(ExportTask, pk=task_id, user=request.user)
    if not task.file:
        raise Http404
    response = HttpResponse(task.file.read(), mimetype="application/octet-stream")
    response["Content-Disposition"] = 'attachment; filename="bookmarks.html"'
    return response


class BookmarkletsView(TemplateView):
    """ Bookmarklets page """
    template_name = "bookmarklets.html"

    def get_context_data(self):
        return {"nav": {"bookmarklets": True}}


class LoginOrRegisterPageView(TemplateView):
    """ Index page to anon
        Login and register form
    """
    template_name = "login_or_register.html"

    def get_context_data(self):
        return {"registration_form" : UserCreationFormWithCaptcha(),
                "login_form" : AuthenticationForm()}


class QRCodeView(DetailView):
    model = Link
    template_name = 'qr_code.html'

    def get_object(self):
        bookmark = super(QRCodeView, self).get_object()
        if bookmark.owner_id != self.request.user.pk:
            raise Http404
        return bookmark


@login_required
@transaction.commit_on_success
def link_delete_batch(request):
    """ Batch delete """
    PER_PAGE = Profile.objects.get_or_create(user=request.user)[0].per_page
    qs = Link.objects.filter(owner=request.user)
    paginator = Paginator(qs, PER_PAGE)
    page_number = request.GET.get('page', 1)
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    formset = LinkDeleteFormSet(
                  request.POST or None,
                  queryset=Link.objects.filter(
                      pk__in=[ i.pk for i in page.object_list ],
                      owner=request.user
                  )
              )
    if formset.is_valid():
        formset.save()
        messages.success(request, _("Bookmarks deleted"))
        return HttpResponseRedirect(reverse("delete_many"))
    c = {"formset" : formset,
         "paginator": paginator,
         "page": page,
         "min_page": page.number - 3,
         "max_page": page.number + 3,
         "nav": {"index": True}}
    return render(request, "link_delete_batch.html", c)


@anonymous_required
def user_create(request):
    """ Registration page """
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
    per_page = Profile.objects.get_or_create(user=request.user)[0].per_page
    c = {"links": links,
         "nav": {"index": True},
         "PER_PAGE": per_page}
    return render(request, "index2.html", c)


@login_required
def link_list_ajax(request):
    """ List of bookmarks

	{"links": [{"pk": self.pk,
                "href": self.href,
                "title": self.title,
                "description": self.description,
                "domain": self.domain(),
                "added": self.added.isoformat()}],
     "meta": {
     }
	}
    """
    page_number = request.GET.get("p", 1)
    query = request.GET.get("q", "").strip()


    links = Link.objects.filter(owner=request.user)
    profile = Profile.objects.get_or_create(user=request.user)[0]

    if query:
        links = links.filter(Q(href__icontains=query) | \
                             Q(title__icontains=query) | \
                             Q(description__icontains=query))
    else:
        links = links.order_by('-pk')
    all_count = links.count()
    paginator = Paginator(links, profile.per_page)
    try:
        page = paginator.page(page_number)
    except:
        logger.exception("paginationg in link_list_ajax")
        page = paginator.page(1)

    links = [i.dict() for i in page.object_list]
    meta = {"page": {"has_next": page.has_next(),
                     "has_previous": page.has_previous(),
                     "current_index": page.number,
                     "per_page": paginator.per_page,
                     "num_pages": paginator.num_pages,
                     "page_range": paginator.page_range},
            "count": all_count}
    data = {"links": links, "meta": meta}
    response = HttpResponse(dumps(data))
    response['Content-Type'] = 'application/json'
    return response


@login_required
@transaction.commit_on_success
def profile_edit(request):
    """ "Settings" page """
    profile = Profile.objects.get_or_create(user=request.user)[0]
    profile_form = ProfileEditForm(request.POST or None,
                                   instance=profile,
                                   prefix="profile")
    import_form = ImportBookmarksForm(request.POST or None,
                                      request.FILES or None,
                                      prefix="import")
    export_form = ExportBookmarksForm(request.POST or None, prefix="export")
    if "settings_form" in request.POST and profile_form.is_valid():
        profile_form.save()
        messages.success(request, _("Settings saved"))
        return redirect("/")
    if "import_form" in request.POST and import_form.is_valid():
        task = import_form.save(commit=False)
        task.user = request.user
        task.save()
        messages.success(request, _("Import task added. It will be processed shortly."))
        return redirect("settings")
    if "export_form" in request.POST and export_form.is_valid():
        task = export_form.save(commit=False)
        task.user = request.user
        task.save()
        messages.success(request, _("Export task added. It will be processed shortly."))
        return redirect("settings")
    c = {
        "profile": profile,
        "profile_form": profile_form,
        "import_form": import_form,
        "import_tasks": ImportTask.objects.filter(user=request.user, added__gt=datetime.now() - timedelta(days=7)),
        "export_form": export_form,
        "export_tasks": ExportTask.objects.filter(user=request.user, added__gt=datetime.now() - timedelta(days=7)),
        "nav": { "settings": True },
    }
    return render(request, "profile_edit.html", c)


@login_required
def link_search(request):
    """
        Ajax handler to load search
    """
    q = request.GET.get("q", "").strip()
    links = Link.objects.filter(owner=request.user)
    if q:
        links = links.filter(Q(href__icontains=q) | \
                             Q(title__icontains=q) | \
                             Q(description__icontains=q))
    else:
        links = links.order_by('-pk')
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
    request = LinkForm.check_encoding(request)
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

