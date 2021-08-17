import os
import sys

from django.test import TestCase


class StorageManagerUnittest(TestCase):
    CONFIG_FILE_ROOT: str = ["server", "config.json"]
    token: str = '\\' if sys.platform == 'win32' else '/'

    @classmethod
    def setUpClass(cls):
        super(StorageManagerUnittest, cls).setUpClass()

        config_file_root_str = os.path.join(*StorageManagerUnittest.CONFIG_FILE_ROOT)
        if not os.path.isfile(config_file_root_str):
            raise FileNotFoundError("Config File Not Found")
