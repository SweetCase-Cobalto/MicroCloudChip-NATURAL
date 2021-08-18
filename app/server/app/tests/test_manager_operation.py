from django.test import TestCase

import os

from module.specification.System_config import SystemConfig


class ManagerOperationUnittest(TestCase):
    # API 없이 서버 프로세스를 테스트합니다.

    config: SystemConfig = SystemConfig(os.path.join(*["server", "config.json"]))
    root_token: config.get_system_root()
    user_manager: UserManager = None
    storage_manager: StorageManager = None

    def setUp(self) -> None:
        self.user_manager = UserManager(self.config)
        # 초기화를 할 때 UserManager 는 Admin 이 있는 지 확인한다.
        # 없을 경우 config information 을 확인하여 Admin User 를 생성한다.
        self.storage_manager = StorageManager(self.config)

    # User Test
    def test_add_user(self):
        pass

    def tearDown(self) -> None:
        pass

    @classmethod
    def tearDownClass(cls):
        pass
