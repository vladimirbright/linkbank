# coding: utf8

from os import environ
from urlparse import urlparse


from settings import *

db = environ['DB_PORT']
db = urlparse(db)

DATABASES['default']['HOST'] = db.hostname
DATABASES['default']['PORT'] = db.port
