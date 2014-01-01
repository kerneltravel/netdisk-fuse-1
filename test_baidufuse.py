from stat import S_IFDIR, S_IFREG
from testtools import TestCase
from testtools.matchers import *
from baidufuse import BaiDuFuse


class BaiDuFuseTest(TestCase):

    def setUp(self):
        """Name: netfuse-tests
        API key: Xmn2E0iwEkqbilNhiw5CctKO
        get access token from
        https://openapi.baidu.com/oauth/2.0/authorize?response_type=token&client_id=Xmn2E0iwEkqbilNhiw5CctKO&redirect_uri=oob&scope=netdisk"""

        super(BaiDuFuseTest, self).setUp()
        self.fuse = BaiDuFuse("23.f8535b8638ab1f208eb791b9b00c2433.2592000.1391152090.637842411-2040226", "netfuse-test")

    def test_get_disk_quote(self):
        statfs = self.fuse.statfs(".")

        self.assertThat(statfs["f_bsize"], Equals(4096))
        self.assertThat(statfs["f_blocks"], GreaterThan(0))
        self.assertThat(statfs["f_bavail"], GreaterThan(0))

    def test_read_dir_and_return_files(self):
        files = self.fuse.readdir(".", None)

        self.assertThat(files, ContainsAll([".", "..", "testdir", "file1.txt", "file2.txt"]))

    def test_read_sub_dir_and_return_files(self):
        files = self.fuse.readdir("/testdir", None)

        self.assertThat(files, ContainsAll([".", "..", "dir_file1.txt", "dir_file2.txt"]))

    def test_get_attr_for_current_directory(self):
        attr = self.fuse.getattr("/")

        self.assertThat(attr['st_mode'], Equals(S_IFDIR | 0755))
        self.assertThat(attr['st_nlink'], Equals(2))

    def test_get_attr_for_sub_directory(self):
        attr = self.fuse.getattr("/testdir")

        self.assertThat(attr['st_mode'], Equals(S_IFDIR | 0755))
        self.assertThat(attr['st_nlink'], Equals(2))

    def test_get_attr_for_files(self):
        attr = self.fuse.getattr("/file1.txt")

        self.assertThat(attr['st_mode'], Equals(S_IFREG | 0777))
        self.assertThat(attr['st_nlink'], Equals(1))
        self.assertThat(attr['st_size'], Equals(22))

    def test_get_attr_for_files_in_sub_folder(self):
        attr = self.fuse.getattr("/testdir/dir_file1.txt")

        self.assertThat(attr['st_mode'], Equals(S_IFREG | 0777))
        self.assertThat(attr['st_nlink'], Equals(1))
        self.assertThat(attr['st_size'], Equals(27))
