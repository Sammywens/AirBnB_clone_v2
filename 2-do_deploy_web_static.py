#!/usr/bin/python3
from fabric.api import run, local, env, put
from datetime import datetime
from os import path
from fabric.context_managers import cd

env.hosts = ['54.237.209.240', '54.198.28.227']
env.user = 'ubuntu'
env.key_filename = '/root/.ssh/school'


def do_deploy(archive_path):
    """Distributes an archive to web servers"""
    if not path.exists(archive_path):
        return False

    # Upload the archive to the /tmp/ directory of the web server
    put(archive_path, "/tmp/")

    # Uncompress the archive to /data/web_static/releases/
    archive_filename = archive_path.split("/")[-1]
    archive_basename = archive_filename.split(".")[0]
    release_dir = "/data/web_static/releases/" + archive_basename
    run("sudo mkdir -p {}".format(release_dir))
    run("sudo tar -xzf /tmp/{} -C {}".format(archive_filename, release_dir))
    run("sudo rm /tmp/{}".format(archive_filename))
    run("sudo mv {}/web_static/* {}/".format(release_dir, release_dir))
    run("sudo rm -rf {}/web_static".format(release_dir))

    # Update the symbolic link
    current_dir = "/data/web_static/current"
    run("sudo rm -f {}".format(current_dir))
    run("sudo ln -s {} {}".format(release_dir, current_dir))

    return True
