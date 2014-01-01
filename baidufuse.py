import logging
from sys import argv, exit

from fuse import FUSE, Operations, LoggingMixIn
from baidupcs import PCS


class BaiDuFuse(LoggingMixIn, Operations):
    def __init__(self, accessToken, basedir):
        self.pcs = PCS(accessToken)
        self.appdir = "/apps/" + basedir + "/"

    def statfs(self, path):
        disk_info = self.pcs.info().json()
        bsize = 4096
        total = disk_info['quota'] / bsize
        used = disk_info['used'] / bsize
        free = total - used

        free_files = 1024
        return dict(f_bsize=bsize, f_frsize=bsize, f_blocks=total, f_bavail=free, f_bfree=free,
                    f_files=free_files, f_ffree=free_files, f_favail=free_files)

    def readdir(self, path, fh):
        response = self.pcs.list_files(self.appdir)

        files = ['.', '..']
        for file in response.json()['list']:
            files.append(file['path'].replace(self.appdir, ''))

        return files


if __name__ == '__main__':
    if len(argv) != 4:
        print('usage: %s <mountpoint> "accesstoken" "appdir"' % argv[0])
        exit(1)

    logging.getLogger().setLevel(logging.DEBUG)
    fuse = FUSE(BaiDuFuse(argv[2], argv[3]), argv[1], foreground=True)