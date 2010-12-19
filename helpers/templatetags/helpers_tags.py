# -*- coding: utf-8 -*-

from django import template

register = template.Library()


@register.inclusion_tag("_form.html")
def render_form(form):
    return { "form": form }
