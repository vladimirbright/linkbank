# -*- coding: utf-8 -*-

from fabric.api import *
from fabric.contrib.console import confirm
from fabric.utils import abort


@hosts('knbase.info@knbase.info')
def ppull():
    u""" git pull on developer@192.168.0.103"""
    with cd('~/linkbank'):
        run('git pull', pty=True)


@hosts('knbase.info@knbase.info')
def prestart():
    with cd('~'):
        run('kill -HUP `cat django.pid`')


def update():
    ppull()
    prestart()
