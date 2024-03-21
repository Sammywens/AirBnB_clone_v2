#!/usr/bin/python3
import os
from fabric.api import env
from fabric.api import local
from fabric.api import put
from fabric.api import run

env.hosts = ['54.237.209.240', '54.198.28.227']
env.key_filename = '/root/.ssh/school'


def do_clean(number=0):
    """Delete out-of-date archives.

    Args:
        number(int): The number of archives to keep.

    If number is 0 or 1, keeps only the most recent archive. If
    number is 2, keeps the most and second-most recent archives,
    etc.
    """
    num_files = local("ls -1t versions/ | wc -l", capture=True)
    if number == "0":
        number = "1"
    sub = int(num_files) - int(number)
    if sub > 0:
        for i in range(0, sub):
            local("rm  versions/$(ls -1t versions/ | tail -1)")
