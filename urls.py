# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'bank.views.link_list'),
    url(r'^(\d+)/delete/$', 'bank.views.link_delete'),
    url(r'^(\d+)/edit/$', 'bank.views.link_edit'),
    url(r'^add/$', 'bank.views.link_create'),
    url(r'^signup/$', 'bank.views.user_create'),
    url(r'^signin/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^signout/$', 'django.contrib.auth.views.logout',
                                          { "next_page": "/" }, name='logout'),
    url(r'^captcha/', include('captcha.urls')),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)
