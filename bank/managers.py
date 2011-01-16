# -*- coding: utf-8 -*-

from collections import Iterable
from sphinxapi import SphinxClient

from django.conf import settings
from django.db.models import Manager


_SPHINXS = settings.SPHINXS

class SearchManager(Manager):
    """Simple manager to search with sphinx search engine """
    _host = None
    _port = None
    _client = None
    _total_found = 0
    _index = None

    def __init__(self, index, using="default"):
        self._host = _SPHINXS[using][0]
        self._port = _SPHINXS[using][1]
        self._index = index
        self._client = SphinxClient()
        self._client.SetServer(self._host, self._port)
        self._total_found = 0
        super(SearchManager, self).__init__()

    @property
    def sphinx(self):
        return self._client

    @property
    def index(self):
        return self._index

    @property
    def total_found(self):
        return self._total_found

    def query(self, query):
        query = self._client.EscapeString(query)
        _r = self._client.Query(query, self._index)
        if not _r or \
           not "matches" in _r or \
           not _r["matches"]:
            return self.none()
        _ids = [ int(m["id"]) for m in _r["matches"] ]
        _qs = self.filter(pk__in=_ids)
        for o in _qs:
            try:
                _ids[_ids.index(o.pk)] = o
            except(ValueError, IndexError):
                continue
        self._total_found = _r["total_found"]
        return _ids

