# -*- coding: utf-8 -*-

from django import template

register = template.Library()

@register.filter
def qr(value,size="150x150"):
    """
        Usage:
            <img src="{{object.code|qr:"120x130"}}" />
    """
    return "http://chart.apis.google.com/chart?chs=%s&cht=qr&chl=%s&choe=UTF-8&chld=H|0" % (size, value)

@register.filter
def multiple(a, b):
    return a * b

@register.filter
def sum(a, b):
    return a + b


@register.inclusion_tag("_form.html")
def render_form(form):
    return { "form": form }
