# -*- coding: utf-8 -*-

from fabric.api import *
# from fabric.contrib.console import confirm
# from fabric.utils import abort


env.project_dir = "/home/knbase.info/linkbank"
env.home_dir = "/home/knbase.info"


@hosts('knbase.info@knbase.info')
def git_pull():
    with cd(env.project_dir):
        run('git pull', pty=True)


@hosts('knbase.info@knbase.info')
def django_hup():
    run('kill -HUP `cat ' + env.home_dir + '/django.pid`', pty=True)


@hosts('root@knbase.info')
def django_stop():
    run('supervisorctl stop knbase.info', pty=True)


@hosts('root@knbase.info')
def django_start():
    run('supervisorctl start knbase.info', pty=True)


@hosts('root@knbase.info')
def django_restart():
    run('supervisorctl restart knbase.info', pty=True)


@hosts('root@knbase.info')
def django_status():
    run('supervisorctl status knbase.info', pty=True)


@hosts('knbase.info@knbase.info')
def update():
    git_pull()
    django_hup()

