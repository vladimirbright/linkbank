# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext


def link_list(request):
    c = {}
    return render_to_response("index.html", c,
                              context_instance=RequestContext(request))


@login_required
def link_delete(request, l_id):
    return HttpResponse('b')


@login_required
def link_create(request):
    return HttpResponse('c')

