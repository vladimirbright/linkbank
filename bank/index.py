# -*- coding: utf-8 -*-
from djapian import space, Indexer

from bank.models import Link


class LinkIndexer(Indexer):
    fields = ['href', 'title', 'description']
    tags = [
        ('title', 'title'),
        ('owner', 'owner'),
    ]

space.add_index(Link, LinkIndexer, attach_as='indexer')

