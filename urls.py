# -*- coding: utf-8 -*-

from django.conf.urls.defaults import url, patterns, include
from django.contrib import admin
from django.views.generic import TemplateView
# from django.conf import settings
import djapian

djapian.load_indexes()


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'bank.views.link_list', name="index"),
    url(r'^search/$', 'bank.views.link_search'),
    url(r'^(\d+)/delete/$', 'bank.views.link_delete', name="delete"),
    url(r'^(\d+)/edit/$', 'bank.views.link_edit', name="edit"),
    url(r'^add/$', 'bank.views.link_create'),
    url(r'^new/$', 'bank.views.link_create_extended', name="new"),
    url(r'^signup/$', 'bank.views.user_create', name="signup"),
    url(r'^signin/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^signout/$', 'django.contrib.auth.views.logout', { "next_page": "/" }, name='logout'),
    url(r'^ok$', TemplateView.as_view(template_name="ok.html"), name="ok"),
    url(r'^captcha/', include('captcha.urls')),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)
