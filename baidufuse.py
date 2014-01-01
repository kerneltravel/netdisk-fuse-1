import logging

from fuse import FUSE, FuseOSError, Operations, LoggingMixIn
from baidupcs import PCS
from sys import argv, exit


class BaiDuFuse(LoggingMixIn, Operations):
    def __init__(self, accessToken, basedir):
        self.pcs = PCS(accessToken)
        self.appdir = "/apps/" + basedir + "/"

    def statfs(self, path):
        return dict(f_bsize=512, f_blocks=4096, f_bavail=2048)

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