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

    def test_read_dir_and_return_files(self):
        files = self.fuse.readdir(".", "")
        self.assertThat(len(files), NotEquals(0))
        self.assertThat(files[0], Equals("."))
        self.assertThat(files[1], Equals(".."))
