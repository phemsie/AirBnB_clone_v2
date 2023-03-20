#!/usr/bin/python3
# a Fabric script that generates a .tgz archive from web_static folder

from fabric.api import local
from datetime import datetime


def do_pack():
    ''' generates a .tgz archive from the contents '''
    dt_now = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    archive_path = "versions/web_static_{}.tgz".format(dt_now)
    cmd_compress = "tar -cvzf {} web_static/".format(archive_path)
    local("mkdir -p versions")
    archived = local(cmd_compress)
    if archived.failed:
        return None
    return archive_path
