import sys
from django.test import TestCase
import os

from module.MicrocloudchipException.exceptions import MicrocloudchipAuthAccessError, \
    MicrocloudchipFileAlreadyExistError, MicrocloudchipDirectoryAlreadyExistError, \
    MicrocloudchipStorageOverCapacityError

from module.manager.storage_manager import StorageManager
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
    SYSTEM_ROOT: str = config.get_system_root()
    IMG_EXAMPLE_ROOT: str = os.path.join(*["app", "tests", "test-input-data", "user", "example.png"])
    token: str = '\\' if sys.platform == 'win32' else '/'

    user_manager: UserManager = None
    storage_manager: StorageManager = None

    # 테스트 대상 Users
    admin_static_id: str = ""
    client_static_id: str = ""
    other_static_id: str = ""

    # 테스트 파일이 들어있는 루트
    TEST_FILE_ROOT: str = "app/tests/test-input-data/example_files"
    TEST_FILES: str = os.listdir(TEST_FILE_ROOT)

    def setUp(self) -> None:

        self.user_manager = UserManager(self.config)
        # 초기화를 할 때 UserManager 는 Admin 이 있는 지 확인한다.
        # 없을 경우 config information 을 확인하여 Admin User 를 생성한다.

        self.storage_manager = StorageManager(self.config)

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
            "volume-type": "GUEST",
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

        # 클라이언트 이미지가 들어가 있는 루트
        client_img_root = os.path.join(self.config.get_system_root(), "storage", self.client_static_id, 'asset',
                                       'user.png')

        # 삭제 전
        self.assertTrue(os.path.isfile(client_img_root))

        # 이미지 삭제
        # img-raw-data 가 None -> 이미지 삭제
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

    def test_add_datas(self):
        """ File/Directory 권한에 따른 저장 """

        ex_filename: str = self.TEST_FILES[0]
        raw: bytes = read_test_file(os.path.join(self.TEST_FILE_ROOT, ex_filename))

        file_add_req = {
            "static-id": self.admin_static_id,
            "target-root": self.TEST_FILES[0],
            "raw-data": raw
        }
        dir_add_req = {
            "static-id": self.admin_static_id,
            "target-root": "test-dir"
        }

        # File Checking
        self.storage_manager.upload_file(
            self.admin_static_id,
            file_add_req,
            self.user_manager
        )
        self.assertTrue(
            os.path.isfile(
                os.path.join(self.SYSTEM_ROOT, 'storage', self.admin_static_id,
                             'root', file_add_req['target-root'])
            )
        )

        # Directory Checking
        self.storage_manager.generate_directory(
            self.admin_static_id,
            dir_add_req
        )
        self.assertTrue(
            os.path.isdir(
                os.path.join(self.SYSTEM_ROOT, 'storage', self.admin_static_id,
                             'root', dir_add_req['target-root'])
            )
        )

        """ 다른 사용자가 파일및 디렉토리를 추가할 수 없다"""
        self.assertRaises(
            MicrocloudchipAuthAccessError,
            lambda: self.storage_manager.upload_file(
                self.client_static_id,
                file_add_req,
                self.user_manager
            )
        )
        self.assertRaises(
            MicrocloudchipAuthAccessError,
            lambda: self.storage_manager.generate_directory(
                self.client_static_id,
                dir_add_req,
            )
        )

        """동일 파일 및 폴더는 생성 불가"""
        self.assertRaises(
            MicrocloudchipFileAlreadyExistError,
            lambda: self.storage_manager.upload_file(
                self.admin_static_id,
                file_add_req,
                self.user_manager
            )
        )
        self.assertRaises(
            MicrocloudchipDirectoryAlreadyExistError,
            lambda: self.storage_manager.generate_directory(
                self.admin_static_id,
                dir_add_req,
            )
        )

        """사용량 초과 시 알림"""
        file_add_req['static-id'] = self.client_static_id
        # 테스트용 클라이언트는 최대 사용 가능 용량이 1KB

        self.assertRaises(
            MicrocloudchipStorageOverCapacityError,
            lambda: self.storage_manager.upload_file(
                self.client_static_id,
                file_add_req,
                self.user_manager
            )
        )

    def test_update_datas(self):

        ex_filename: str = self.TEST_FILES[0]
        raw: bytes = read_test_file(os.path.join(self.TEST_FILE_ROOT, ex_filename))

        # 파일과 디렉토리 생성
        file_add_req = {
            "static-id": self.admin_static_id,
            "target-root": ex_filename,
            "raw-data": raw
        }
        dir_add_req = {
            "static-id": self.admin_static_id,
            "target-root": "test-dir"
        }

        test_file_ex: str = ex_filename.split('.')[-1]
        self.storage_manager.upload_file(self.admin_static_id, file_add_req, self.user_manager)

        self.storage_manager.generate_directory(self.admin_static_id, dir_add_req)

        # 파일 및 디렉토리 수정
        file_update_req = {
            "static-id": self.admin_static_id,
            "target-root": ex_filename,
            "change": {
                "name": "reddd." + test_file_ex
            }
        }
        dir_update_req = {
            "static-id": self.admin_static_id,
            "target-root": "test-dir",
            "change": {
                "name": "other-dir"
            }
        }

        self.storage_manager.update_file(self.admin_static_id, file_update_req)
        self.storage_manager.update_directory(self.admin_static_id, dir_update_req)

        """ 동일한 파일 이름을 수정 할 때 존재하는 파일 및 디렉토리 이름으로 수정이 불가능하다. """
        self.storage_manager.upload_file(self.admin_static_id, file_add_req, self.user_manager)
        self.storage_manager.generate_directory(self.admin_static_id, dir_add_req)

        self.assertRaises(
            MicrocloudchipFileAlreadyExistError,
            lambda: self.storage_manager.update_file(self.admin_static_id, file_update_req)
        )
        self.assertRaises(
            MicrocloudchipDirectoryAlreadyExistError,
            lambda: self.storage_manager.update_directory(self.admin_static_id, dir_update_req)
        )

        file_update_req['change']['name'] = "xx" + test_file_ex
        dir_update_req['change']['name'] = "ch-dir"

        """ 다른 계정이 변경을 시도하면 안된다 """
        self.assertRaises(
            MicrocloudchipAuthAccessError,
            lambda: self.storage_manager.update_file(self.client_static_id, file_update_req)
        )
        self.assertRaises(
            MicrocloudchipAuthAccessError,
            lambda: self.storage_manager.update_directory(self.client_static_id, dir_update_req)
        )

    def test_get_list_in_directory(self):

        # 상위 디렉토리 생성
        dir_format: dict = {
            "static-id": self.admin_static_id,
            "target-root": "test-dir"
        }
        self.storage_manager.generate_directory(self.admin_static_id, dir_format)

        # 디렉토리들 생성
        sub_dir_name = ['d01', 'd02', 'd03']
        for d in sub_dir_name:
            dir_format['target-root'] = os.path.join('test-dir', d)
            self.storage_manager.generate_directory(self.admin_static_id, dir_format)

        # 파일 하나 생성
        ex_filename: str = self.TEST_FILES[0]
        raw: bytes = read_test_file(os.path.join(self.TEST_FILE_ROOT, ex_filename))

        file_format: dict = {
            "static-id": self.admin_static_id,
            "target-root": os.path.join('test-dir', ex_filename),
            "raw-data": raw
        }
        self.storage_manager.upload_file(self.admin_static_id, file_format, self.user_manager)

        # 데이터 요청 포맷
        req_format: dict = {
            "static-id": self.admin_static_id,
            "target-root": 'test-dir'
        }
        file_list, directory_list = self.storage_manager.get_data(self.admin_static_id, req_format)

        # 검색된 디렉토리 이름 리스트
        checked_dir_list: list[str] = [a.name for a in directory_list]

        # 측정
        self.assertEqual(file_list[0].name, ex_filename)
        self.assertCountEqual(sub_dir_name, checked_dir_list)

        # 다른 사용자가 접근해서는 안된다
        self.assertRaises(
            MicrocloudchipAuthAccessError,
            lambda: self.storage_manager.get_data(self.client_static_id, req_format)
        )

    def test_delete_datas(self):

        """ Info: Raw 단계와는 달리 Manager 단위에서는 디렉토리를 삭제할 때
            Recursive 하게 삭제합니다.
        """

        # 상위 디렉토리 생성
        dir_format: dict = {
            "static-id": self.admin_static_id,
            "target-root": "test-dir"
        }
        self.storage_manager.generate_directory(self.admin_static_id, dir_format)

        # 디렉토리들 생성
        sub_dir_name = ['d01', 'd02', 'd03']
        for d in sub_dir_name:
            dir_format['target-root'] = os.path.join('test-dir', d)
            self.storage_manager.generate_directory(self.admin_static_id, dir_format)

        # 파일 하나 생성
        ex_filename: str = self.TEST_FILES[0]
        raw: bytes = read_test_file(os.path.join(self.TEST_FILE_ROOT, ex_filename))

        file_format: dict = {
            "static-id": self.admin_static_id,
            "target-root": os.path.join('test-dir', ex_filename),
            "raw-data": raw
        }
        self.storage_manager.upload_file(self.admin_static_id, file_format, self.user_manager)

        req_dir_delete_format: dict = {
            'static-id': self.admin_static_id,
            'target-root': 'test-dir'
        }

        # 다른 계정이 함부로 삭제할 수 없다
        self.assertRaises(
            MicrocloudchipAuthAccessError,
            lambda: self.storage_manager.delete_directory(self.client_static_id, req_dir_delete_format)
        )

        # 제대로 된 삭제
        self.storage_manager.delete_directory(self.admin_static_id, req_dir_delete_format)
        f_list, d_list = self.storage_manager.get_data(self.admin_static_id, {
            'static-id': self.admin_static_id,
            'target-root': ''
        })

        self.assertEqual(len(f_list), 0)
        self.assertEqual(len(d_list), 0)

    def test_delete_user(self):
        # 데이터 생성
        # 상위 디렉토리 생성
        dir_format: dict = {
            "static-id": self.admin_static_id,
            "target-root": "test-dir"
        }
        self.storage_manager.generate_directory(self.admin_static_id, dir_format)

        # 디렉토리들 생성
        sub_dir_name = ['d01', 'd02', 'd03']
        for d in sub_dir_name:
            dir_format['target-root'] = os.path.join('test-dir', d)
            self.storage_manager.generate_directory(self.admin_static_id, dir_format)

        # 파일 하나 생성
        ex_filename: str = self.TEST_FILES[0]
        raw: bytes = read_test_file(os.path.join(self.TEST_FILE_ROOT, ex_filename))

        file_format: dict = {
            "static-id": self.admin_static_id,
            "target-root": os.path.join('test-dir', ex_filename),
            "raw-data": raw
        }
        self.storage_manager.upload_file(self.admin_static_id, file_format, self.user_manager)

        # Admin 만 삭제할 수 있다.
        self.assertRaises(
            MicrocloudchipAuthAccessError,
            lambda: self.user_manager.delete_user(
                self.client_static_id, self.other_static_id, self.storage_manager
            )
        )

        # 삭제
        self.user_manager.delete_user(self.admin_static_id, self.other_static_id, self.storage_manager)