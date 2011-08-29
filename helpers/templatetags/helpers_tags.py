# -*- coding: utf-8 -*-
import re

from django import template
from django.template.defaultfilters import linebreaks, escape, safe

register = template.Library()

HASHTAG_PATTERN = re.compile(r'#([\S]+)', re.U + re.I)

@register.filter
def link_body(body):
    return safe(linebreaks(HASHTAG_PATTERN.sub(r"<a class='hash_tag' href='#q=\1'>#\1</a>", escape(body))))


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
