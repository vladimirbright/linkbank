# -*- coding: utf-8 -*-

from fabric.api import *
# from fabric.contrib.console import confirm
# from fabric.utils import abort


env.project_dir = "/home/knbase.info/linkbank"
env.home_dir = "/home/knbase.info"
env.manage = env.project_dir + "/manage.py"
env.activate = env.home_dir + "/ve/bin/activate"


def cc(output_style="compressed"):
    """
        Local compile by compass
    """
    local("compass compile -s %s --force" %output_style)


@hosts('knbase.info@knbase.info')
def pull():
    """
        Go to knbase.info and git pull
    """
    with cd(env.project_dir):
        run('git pull', pty=True)


@hosts('knbase.info@knbase.info')
def hup():
    run('kill -HUP `cat ' + env.home_dir + '/django.pid`', pty=True)


@hosts('root@knbase.info')
def stop():
    run('supervisorctl stop knbase.info', pty=True)


@hosts('root@knbase.info')
def start():
    run('supervisorctl start knbase.info', pty=True)


@hosts('root@knbase.info')
def restart():
    run('supervisorctl restart knbase.info', pty=True)


@hosts('root@knbase.info')
def status():
    run('supervisorctl status knbase.info', pty=True)


@hosts('knbase.info@knbase.info')
def manage(command=""):
    if not command:
        raise ValueError, "specify command"
    with cd(env.project_dir):
        run("source " + env.activate + " && python " + env.manage + " " + command , pty=True)


@hosts('knbase.info@knbase.info')
def update():
    pull()
    hup()


@hosts('knbase.info@knbase.info')
def mupdate():
    pull()
    manage("migrate --all")
    hup()

