# -*- coding: utf-8 -*-

from fabric.api import *
# from fabric.contrib.console import confirm
# from fabric.utils import abort


env.project_dir = "/home/knbase.info/linkbank"
env.home_dir = "/home/knbase.info/linkbank"


@hosts('knbase.info@knbase.info')
def ppull():
    u""" git pull on developer@192.168.0.103"""
    with cd(env.project_dir):
        run('git pull', pty=True)


@hosts('knbase.info@knbase.info')
def prestart():
    run('kill -HUP `cat ' + env.home_dir + '/django.pid`')


@hosts('knbase.info@knbase.info')
def killall():
    run('killall python')


@hosts('knbase.info@knbase.info')
def update():
    ppull()
    killall()
