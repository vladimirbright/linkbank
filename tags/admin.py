# -*- coding: utf-8 -*-

from django.contrib import admin

from tags.models import *

class TagAdmin(admin.ModelAdmin):
    pass
admin.site.register(Tag, TagAdmin)

