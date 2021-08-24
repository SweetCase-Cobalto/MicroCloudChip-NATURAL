import os

from django.test import TestCase, Client
from django.http.response import JsonResponse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files import File

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

    USR_IMG_ROOT: str = 'app/tests/test-input-data/user/example.png'
    FILES_ROOT: str = 'app/tests/test-input-data/example_files'

    @classmethod
    def setUpClass(cls) -> None:
        super(TestAPIUnittest, cls).setUpClass()

        # Admin
        SYSTEM_CONFIG = SystemConfig("server/config.json")
        UserManager(SYSTEM_CONFIG)
        StorageManager(SYSTEM_CONFIG)

    @staticmethod
    def make_uploaded_file(root: str):
        f: File = File(open(root, 'rb'))
        u: SimpleUploadedFile = SimpleUploadedFile(
            f.name, f.read(), content_type='multipart/form-data'
        )
        return u

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
        # 로그인이 안 된 상태에서 수행 불가
        response = self.client.post(
            '/server/user', {
                'req-static-id': self.admin_static_id,
                'name': 'the-client',
                'email': 'napalosense@gmail.com',
                'password': '098765432',
                'volume-type': 'TEST',
                'img': TestAPIUnittest.make_uploaded_file(self.USR_IMG_ROOT)
            }
        )
        self.assertEqual(response.json()['code'], MicrocloudchipLoginConnectionExpireError("").errorCode)

        # Admin Login
        response = self.client.post(
            '/server/user/login',
            dict(email='seokbong60@gmail.com', pswd='12345678')
        )
        self.assertEqual(response.json()['code'], 0)

        # 유저 생성

        # Success
        response = self.client.post(
            '/server/user', {
                'req-static-id': self.admin_static_id,
                'name': 'theclient',
                'email': 'napalosense@gmail.com',
                'password': '098765432',
                'volume-type': 'TEST',
                'img': TestAPIUnittest.make_uploaded_file(self.USR_IMG_ROOT)
            }
        )
        self.assertEqual(response.json()['code'], 0)

        # Failed[Same email]
        response = self.client.post(
            '/server/user', {
                'req-static-id': self.admin_static_id,
                'name': 'theclient2',
                'email': 'napalosense@gmail.com',
                'password': '934852323',
                'volume-type': 'TEST',
            }
        )
        self.assertEqual(response.json()['code'], MicrocloudchipAuthAccessError("").errorCode)

        # 테스트용 클라리언트 고정 아이디를 구해보자
        client_static_id: str = model.User.objects.get(is_admin=False).static_id

        # 데이터 수정 -> 이름 바꾸기

        response = self.client.put(
            f"/server/user/{client_static_id}", {
                'req-static=id': self.admin_static_id,
                'change-data': {
                    'name': 'sclient2',
                    'img-changeable': False
                }
            }
        )
        # self.assertEqual(response.json()['code'], 0)
