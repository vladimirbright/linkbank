# -*- coding: utf-8 -*-

from django.contrib import admin

from bank.models import *

class LinkAdmin(admin.ModelAdmin):
    pass
admin.site.register(Link, LinkAdmin)

