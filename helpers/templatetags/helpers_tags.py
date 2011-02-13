# -*- coding: utf-8 -*-

from django import template

register = template.Library()

@register.filter
def multiple(a, b):
    return a * b

@register.inclusion_tag("_form.html")
def render_form(form):
    return { "form": form }
