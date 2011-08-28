# -*- coding: utf-8 -*-

from django.contrib import admin

from bank.models import Link, Profile

class LinkAdmin(admin.ModelAdmin):
    pass
admin.site.register(Link, LinkAdmin)
admin.site.register(Profile, LinkAdmin)

