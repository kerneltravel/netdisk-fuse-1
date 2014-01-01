from errno import ENOENT
import logging
from os.path import *
from stat import S_IFDIR, S_IFREG
from sys import argv, exit

from fuse import FUSE, Operations, LoggingMixIn, FuseOSError
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
        dirpath = normpath(self.appdir + path)
        filelist = self.pcs.list_files(dirpath).json()['list']

        files = ['.', '..']
        for file in filelist:
            files.append(basename(file['path']))

        return files

    def getattr(self, path, fh=None):
        print path

        dir_attr = dict(st_mode=(S_IFDIR | 0755), st_nlink=2)
        if path == '/':
            return dir_attr

        filelist = self.pcs.list_files(normpath(self.appdir + dirname(path))).json()['list']

        for file in filelist:
            file_path = file['path']
            if file_path != normpath(self.appdir + "/" + path):
                continue

            if file['isdir'] == 1:
                return dir_attr

            return dict(st_mode=(S_IFREG | 0777), st_nlink=1, st_size=file['size'])

        raise FuseOSError(ENOENT)


if __name__ == '__main__':
    if len(argv) != 4:
        print('usage: %s <mountpoint> "accesstoken" "appdir"' % argv[0])
        exit(1)

    logging.getLogger().setLevel(logging.DEBUG)
    fuse = FUSE(BaiDuFuse(argv[2], argv[3]), argv[1], foreground=True)