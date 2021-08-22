from django.test import TestCase, Client
from django.http.response import JsonResponse
from module.MicrocloudchipException.exceptions import *
import json

from module.manager.storage_manager import StorageManager
from module.manager.user_manager import UserManager
from module.specification.System_config import SystemConfig

SYSTEM_CONFIG: SystemConfig
USER_MANAGER: UserManager
STORAGE_MANAGER: StorageManager


class TestAPIUnittest(TestCase):
    client: Client

    @classmethod
    def setUpClass(cls) -> None:
        super(TestAPIUnittest, cls).setUpClass()
        SYSTEM_CONFIG = SystemConfig("server/config.json")
        USER_MANAGER = UserManager(SYSTEM_CONFIG)
        STORAGE_MANAGER = StorageManager(SYSTEM_CONFIG)

    def setUp(self) -> None:
        self.client = Client()

    def test_login_logout(self):

        # Admin 계정으로 로그인

        # False


        response: JsonResponse = self.client.post(
            '/server/user/login',
            json.dumps(
                {"email": "seokbong60@gmail.com",
                 "pswd": "12345678"
                 }
            ),
            content_type='application/json')
        err_code: int = response.json()['code']

        if err_code == MicrocloudchipLoginFailedError("").errorCode:
            print("err")
