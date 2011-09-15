# -*- coding: utf-8 -*-

from django.contrib import admin

from bank.models import Link, Profile
from helpers.decorators import cache_this


class LinkAdmin(admin.ModelAdmin):
    @cache_this(ttl=84000, key_func=lambda obj: "bank.admin.LinkAdmin.username.%s" % obj.owner_id)
    def username(self, obj):
        return obj.owner.username

    def title_or_href(self, obj):
        return obj.title or obj.href
    list_display = ( "title_or_href", "username", "added" )
    search_fields = ( "title", "href", "owner__username" )
    list_filter = ( "added", )
admin.site.register(Link, LinkAdmin)

admin.site.register(Profile, admin.ModelAdmin)

