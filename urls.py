# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'bank.views.link_list'),
    url(r'(\d+)/delete/$', 'bank.views.link_delete'),
    url(r'add/$', 'bank.views.link_create'),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)
