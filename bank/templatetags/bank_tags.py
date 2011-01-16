# -*- coding: utf-8 -*-


from django import template


register = template.Library()

@register.inclusion_tag("bank/_tags.html")
def tags(bookmark):
    if not bookmark.tags_cache:
        return {}
    tags = [ { "pk": i.split("Q")[1], "title": i.split("Q")[0] }\
                                     for i in bookmark.tags_cache.split("\n") ]
    return { "tags": tags }
