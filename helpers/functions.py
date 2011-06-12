# -*- coding: utf-8 -*-


def get_page_from_request(request, page_seg="page"):
    try:
        page = int(request.GET.get("page", 0))
    except ValueError:
        page = 1
    if page <= 0:
        page = 1
    return page


