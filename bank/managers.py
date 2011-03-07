# -*- coding: utf-8 -*-


from sphinxapi import SphinxClient, SPH_SORT_EXTENDED, SPH_MATCH_EXTENDED2

from django.conf import settings
from django.db.models import Manager

__all__ = (
    "SearchManager",
)

_SPHINXS = settings.SPHINXS


class Search(object):
    """Object to incapsulate search functions"""
    _manager = None
    _client = None
    _index = None
    _total_found = 0
    _per_page = 20

    def __init__(self, manager):
        self._client = manager.sphinx
        self._client.SetMatchMode(SPH_MATCH_EXTENDED2)
        self._index = manager.index
        self._manager = manager

    @property
    def client(self):
        return self._client

    def escape(self, query):
        return self._client.EscapeString(query.strip())

    @property
    def total_found(self):
        return self._total_found or 0

    def paginate(self, request, chunk="page"):
        _page = request.GET.get(chunk, 0)
        try:
            _page = int(_page)
        except ValueError:
            _page = 1
        if _page <= 0:
            _page = 1
        _offset = (_page - 1) * self._per_page
        _limit = _page * self._per_page
        self._client.SetLimits(_offset, _limit, _offset + 100)

    def filter(self, *args, **kwargs):
        self._client.SetFilter(*args, **kwargs)

    def order_by(self, field, desc=True):
        _sort = "@id DESC"
        if field:
            _sort = "%s %s" % (field.strip(), "DESC" if desc else "ASC")
        self._client.SetSortMode(SPH_SORT_EXTENDED, _sort.encode("utf8") )

    @property
    def le(self):
        return self._client.GetLastError()

    @property
    def lw(self):
        return self._client.GetLastWarning()

    def query(self, query):
        _r = self._client.Query(query.strip(), self._index)
        if not _r or \
           not "matches" in _r or \
           not _r["matches"]:
            return self._manager.none()
        _ids = [ int(m["id"]) for m in _r["matches"] ]
        _qs = self._manager.filter(pk__in=_ids)
        for o in _qs:
            try:
                _ids[_ids.index(o.pk)] = o
            except (ValueError, IndexError):
                continue
        self._total_found = _r["total_found"]
        return _ids


class SearchManager(Manager):
    """Simple manager to handle sphinxsearch config"""
    _host = None
    _port = None
    _client = None
    _index = None

    def __init__(self, index, using="default"):
        self._host = _SPHINXS[using][0]
        self._port = _SPHINXS[using][1]
        self._index = index
        self._client = SphinxClient()
        self._client.SetServer(self._host, self._port)
        super(SearchManager, self).__init__()

    def get_search_object(self):
        return Search(self)

    @property
    def sphinx(self):
        return self._client

    @property
    def index(self):
        return self._index

