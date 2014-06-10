# -*- coding: utf-8 -*-

from django.conf.urls.defaults import url, patterns, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
# from django.conf import settings

from bank.views import BookmarkletsView
from bank.views import QRCodeView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'bank.views.link_list', name="index"),
    url(r'^search/$', 'bank.views.link_search'),
    url(r'^search/ajax/$', 'bank.views.link_list_ajax'),
    url(r'^settings/$', 'bank.views.profile_edit', name="settings"),
    url(r'^bookmarklets/$', login_required(BookmarkletsView.as_view()), name="bookmarklets"),
    url(r'^give/me/qr/code/(?P<pk>\d+)$', login_required(QRCodeView.as_view()), name="give_me_qr_code"),
    url(r'^(\d+)/delete/$', 'bank.views.link_delete', name="delete"),
    url(r'^(\d+)/edit/$', 'bank.views.link_edit', name="edit"),
    url(r'^batch-delete/$', 'bank.views.link_delete_batch', name="delete_many"),
    url(r'^add/$', 'bank.views.link_create'), # from bookmarklet
    url(r'^new/$', 'bank.views.link_create_extended', name="new"),
    url(r'^signup/$', 'bank.views.user_create', name="signup"),
    url(r'^download/(?P<task_id>\d+)$', 'bank.views.download_exported_file', name="download_exported_file"),
    url(r'^signin/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^signout/$', 'django.contrib.auth.views.logout', { "next_page": "/" }, name='logout'),
    url(r'^ok$', TemplateView.as_view(template_name="ok.html"), name="ok"),
    url(r'^captcha/', include('captcha.urls')),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)
