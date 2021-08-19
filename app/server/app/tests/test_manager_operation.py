import sys

from django.test import TestCase

import os

from module.MicrocloudchipException.exceptions import MicrocloudchipAuthAccessError
from module.manager.user_manager import UserManager
from module.specification.System_config import SystemConfig


def read_test_file(file_root: str) -> bytes:
    r: bytes = b''

    with open(file_root, 'rb') as f:
        while True:
            b = f.readline()
            if not b:
                break
            r += b
    return r


class ManagerOperationUnittest(TestCase):
    # API 없이 서버 프로세스를 테스트합니다.

    config: SystemConfig = SystemConfig(os.path.join(*["server", "config.json"]))
    IMG_EXAMPLE_ROOT: str = os.path.join(*["app", "tests", "test-input-data", "user", "example.png"])
    token: str = '\\' if sys.platform == 'win32' else '/'

    user_manager: UserManager = None
    # storage_manager: StorageManager = None

    # 테스트 대상 Users
    admin_static_id: str = ""
    client_static_id: str = ""
    other_static_id: str = ""

    def setUp(self) -> None:

        self.user_manager = UserManager(self.config)
        # 초기화를 할 때 UserManager 는 Admin 이 있는 지 확인한다.
        # 없을 경우 config information 을 확인하여 Admin User 를 생성한다.

        # self.storage_manager = StorageManager(self.config)

        # admin_static_id 갖고오기
        self.admin_static_id = self.user_manager.get_users()[0].static_id

        # User Add Test 는 여기서 진행한다.

        # 예제 이미지 데이터 추출
        user_req = {
            "name": "client",
            "password": "12346789",
            "email": "napalosense@gmail.com",
            "volume-type": "TEST",
            "img-raw-data": read_test_file(self.IMG_EXAMPLE_ROOT),
            "img-extension": self.IMG_EXAMPLE_ROOT.split(self.token)[-1].split('.')[-1]
        }
        self.user_manager.add_user(self.admin_static_id, user_req)

        # client static_id를 찾기 위해 검색
        for user in self.user_manager.get_users():
            if user.name == 'client':
                self.client_static_id = user.static_id
                break
        self.assertIsNotNone(self.client_static_id)

        # Client 가 User 를 생성하는 일은 없어야 한다
        self.assertRaises(MicrocloudchipAuthAccessError,
                          lambda: self.user_manager.add_user(self.client_static_id, user_req))

        # Client 하나 더 생성
        # 이미지 추가
        other_client_req = {
            "name": "other",
            "password": "12346789",
            "email": "napalosense2@gmail.com",
            "volume-type": "TEST",
            "img-raw-data": None,
            "img-extension": None
        }

        # 한 개 더 생성된 유저의 static_id 추출
        self.user_manager.add_user(self.admin_static_id, other_client_req)
        for user in self.user_manager.get_users():
            if user.name == other_client_req['name']:
                self.other_static_id = user.static_id
                break

    def test_user_update(self):
        # User 업데이트 시 반드시 변경되지 말아야 할 부분
        """
            1. email
            2. static_id
        """

        update_req = {
            "static-id": self.client_static_id,
            "name": "sub-client",
            "password": "0987654321",
            "volume-type": "GUEST",
            "img-changeable": False,
            "img-raw-data": None,
            "img-extension": None
        }
        # admin 및 Client 자신이 직접 수정 가능하다.
        self.user_manager.update_user(self.client_static_id, update_req)

        # 어드민도 변경이 가능한 지 확인
        update_req['name'] = "client"
        self.user_manager.update_user(self.admin_static_id, update_req)

        # 다른 Client 가 데이터 수정을 해선 안된다
        update_req['name'] = "client2"
        self.assertRaises(MicrocloudchipAuthAccessError,
                          lambda: self.user_manager.update_user(self.other_static_id, update_req))

        # 이미지 삭제
        client_img_root = os.path.join(self.config.get_system_root(), "storage", self.client_static_id, 'asset',
                                       'user.png')

        # 삭제 전
        self.assertTrue(os.path.isfile(client_img_root))

        update_req['img-changeable'] = True
        self.user_manager.update_user(self.admin_static_id, update_req)

        # 삭제 후
        self.assertFalse(os.path.isfile(client_img_root))

        # 다시 생성
        update_req['img-raw-data'] = read_test_file(self.IMG_EXAMPLE_ROOT)
        update_req['img-extension'] = self.IMG_EXAMPLE_ROOT.split(self.token)[-1].split('.')[-1]

        # 생성 후 체크
        self.user_manager.update_user(self.admin_static_id, update_req)
        self.assertTrue(os.path.isfile(client_img_root))
