#!/usr/bin/python3
from fabric.api import run, env, put, cd
from os import path

env.hosts = ['54.237.209.240', '54.198.28.227']
env.user = 'ubuntu'
env.key_filename = '/root/.ssh/school'


def do_deploy(archive_path):
    """Distributes an archive to web servers"""
    if not path.exists(archive_path):
        return False

    # Upload the archive to the /tmp/ directory of the web server
    put(archive_path, "/tmp/", use_sudo=True)

    # Uncompress the archive to /data/web_static/releases/
    archive_filename = path.basename(archive_path)
    archive_basename = path.splitext(archive_filename)[0]
    release_dir = "/data/web_static/releases/" + archive_basename
    with cd("/tmp/"):
        run("sudo mkdir -p {}".format(release_dir))
        run("sudo tar -xzf {} -C {}".format(archive_filename, release_dir))
        run("sudo rm {}".format(archive_filename))
        run("sudo mv {}/web_static/* {}/".format(release_dir, release_dir))
        run("sudo rm -rf {}/web_static".format(release_dir))

    # Update the symbolic link
    current_dir = "/data/web_static/current"
    with cd("/data/web_static/"):
        run("sudo rm -f {}".format(current_dir))
        run("sudo ln -s {} {}".format(release_dir, current_dir))

    return True
