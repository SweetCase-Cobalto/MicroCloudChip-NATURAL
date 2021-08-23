from django.test import TestCase, Client
from django.http.response import JsonResponse
from django.core.files.uploadedfile import SimpleUploadedFile

import json
import app.models as model

from module.manager.storage_manager import StorageManager
from module.manager.user_manager import UserManager
from module.specification.System_config import SystemConfig
from module.MicrocloudchipException.exceptions import *

SYSTEM_CONFIG: SystemConfig


class TestAPIUnittest(TestCase):
    client: Client
    admin_static_id: str

    USR_IMG_ROOT: str = 'test-input-data/user/example.png'
    FILES_ROOT: str = 'test-input-data/example_files'

    @classmethod
    def setUpClass(cls) -> None:
        super(TestAPIUnittest, cls).setUpClass()

        # Admin
        SYSTEM_CONFIG = SystemConfig("server/config.json")
        UserManager(SYSTEM_CONFIG)
        StorageManager(SYSTEM_CONFIG)

    def setUp(self) -> None:
        self.client = Client()
        self.admin_static_id = model.User.objects.get(is_admin=True).static_id

    def test_login_logout(self):
        # Admin 계정으로 로그인
        # False [KeyError]
        response: JsonResponse = self.client.post('/server/user/login', json.dumps({}),
                                                  content_type='application/json')
        self.assertEqual(response.json()['code'], MicrocloudchipAuthAccessError("").errorCode)

        # False [LoginFailed]
        response = self.client.post(
            '/server/user/login',
            dict(email="seokbong60@gmail.com", pswd="9999999")

        )
        self.assertEqual(response.json()['code'], MicrocloudchipLoginFailedError("").errorCode)

        # Success
        # 단 install.pl 에서 설정한 이메일을 입력해야 success 가 나온다.
        # 패스워드는 12345678 동일
        response = self.client.post(
            '/server/user/login',
            dict(email='seokbong60@gmail.com', pswd='12345678')
        )
        self.assertEqual(response.json()['code'], 0)

        # 다시 로그인 불가
        response = self.client.post(
            '/server/user/login',
            dict(email='seokbong60@gmail.com', pswd='12345678')
        )
        self.assertEqual(response.json()['code'], MicrocloudchipAuthAccessError("").errorCode)

        self.client.get(
            '/server/user/logout'
        )

    def test_user_add_and_delete(self):
        # Admin Login

        response = self.client.post(
            '/server/user/login',
            dict(email='seokbong60@gmail.com', pswd='12345678')
        )
        self.assertEqual(response.json()['code'], 0)

        # 유저 생성