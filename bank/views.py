# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ungettext_lazy as _


from bank.models import LinkAddForm, Link, UserCreationFormWithCaptcha


def user_create(request):
    if request.user.is_anonymous() is False:
        return HttpResponseRedirect('/')
    form = UserCreationFormWithCaptcha(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        user.email = form.cleaned_data["email"]
        user.is_active = True
        user.save()
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
    c = {}
    c["form"] = LinkAddForm(request.GET or None)
    c["links"] = links
    return render_to_response("links/list.html", c,
                              context_instance=RequestContext(request))


@login_required
def link_delete(request, l_id):
    return HttpResponse('b')


@login_required
def link_create(request):
    form = LinkAddForm(request.GET or None)
    if form.is_valid():
        link = form.save(commit=False)
        link.owner = request.user
        if not Link.objects.filter(owner=request.user,
                                   href=link.href).exists():
            link.save()
            _m = "Link in bank!"
            messages.success(request, _m)
        return HttpResponseRedirect(reverse('bank.views.link_list'))
    c = {}
    c["form"] = form
    return render_to_response("error.html", c,
                              context_instance=RequestContext(request))

