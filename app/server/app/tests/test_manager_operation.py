import sys
from django.test import TestCase
import os
import glob
import app.models as model
from app.tests.test_modules.loader import test_flow, TestCaseFlow, TestCaseFlowRunner

from module.MicrocloudchipException.exceptions import *
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
    EXAMPLE_FILES_ROOT: str = "app/tests/test-input-data/example_files/"
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
        self.admin_static_id = self.user_manager.get_users()[0]['static_id']

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
            if user["name"] == 'client':
                self.client_static_id = user["static_id"]
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

        # Admin으로 추가 불가능
        failed_client_req = {
            "name": "admin",
            "password": "12346789",
            "email": "tototo2@gmail.com",
            "volume-type": "GUEST",
            "img-raw-data": None,
            "img-extension": None
        }
        self.assertRaises(MicrocloudchipAuthAccessError,
                          lambda: self.user_manager.add_user(self.admin_static_id, failed_client_req))

        # 한 개 더 생성된 유저의 static_id 추출
        self.user_manager.add_user(self.admin_static_id, other_client_req)
        for user in self.user_manager.get_users():
            if user["name"] == other_client_req['name']:
                self.other_static_id = user["static_id"]
                break

    def change_str_to_static_id(self, key):
        # Json Test Case에 적혀있는 계정명을 static_id로 치환
        """
            매 테스트 마다 static_id는 랜덤하게 바뀌기 때문에
            Json Test Case에서는 고유 static-id를 저장하는 대신에
            식별자를 저장한다.
            해당 함수는 식별자 명에 따라서 static_id로 치환한다.
            예를 들어 식별자가 admin일 경우 admin의 static_id로 변환해 준다
        """

        def __change(key):
            return {
                "admin": self.admin_static_id,
                "client": self.client_static_id,
                "other": self.other_static_id
            }[key]

        return __change(key)

    @test_flow("app/tests/test-input-data/manager_operation/test_user_update.json")
    def test_user_update(self, test_flow: TestCaseFlow):
        # User 업데이트 시 반드시 변경되지 말아야 할 부분
        """
            1. email
            2. static_id
        """

        def __cmd_update_user(
                target_user: str, request_user: str,
                name: str, password: str,
                volume_type: str,
                img_changeable: bool, img_file: str,
                is_succeed: bool, exception_str: str
        ):
            # Test Method: update user

            # user 정보를 변경하기 위해 request를 생성한다
            req = {
                "static-id": self.change_str_to_static_id(target_user),
                "name": name,
                "password": password,
                "volume-type": volume_type,
                "img-changeable": img_changeable
            }

            # 이미지 파일 여부
            if not img_file:
                # 이미지 파일이 없는 경우 None 처리
                req['img-raw-data'], req['img-extension'] = None, None
            else:
                # Raw Data를 불러오고 확장자를 따로 저장
                real_img_root: str = self.EXAMPLE_FILES_ROOT + img_file
                req['img-raw-data'] = read_test_file(real_img_root)
                req['img-extension'] = real_img_root.split("/")[-1].split('.')[-1]

            # 성공 여부
            if is_succeed:
                self.user_manager.update_user(self.change_str_to_static_id(request_user), req)
                # 이미지 삽입/삭제 명령문에 포함될 경우 이미지 파일 존재 여부 확인 필요
                if img_changeable:

                    # user_asset_directory_root: asset 디렉토리 실제 주소
                    user_asset_directory_root = \
                        os.path.join(
                            self.config.get_system_root(), "storage", req['static-id'], 'asset'
                        )
                    if img_file:
                        # 이미지 삽입 및 변경이 명령문이었을 경우
                        self.assertTrue(os.path.isfile(os.path.join(user_asset_directory_root,
                                                                    f"user.{req['img-extension']}")))
                    else:
                        self.assertCountEqual(glob.glob(os.path.join(user_asset_directory_root, "user.*")), [])

            else:
                # 실패 케이스
                try:
                    # 에러 떠야됨
                    self.user_manager.update_user(self.change_str_to_static_id(request_user), req)
                except MicrocloudchipException as e:
                    # 제대로 된 에러가 호출되었는 지 확인
                    self.assertEqual(type(e).__name__, exception_str)
                else:
                    # 그게 아니면 사실 상 잘못 된 것
                    raise AssertionError("This Case must be failed but it passed or other exception\n"
                                         f"req: {req}")

        # 테스팅 프로세스 실행
        runner: TestCaseFlowRunner = TestCaseFlowRunner(test_flow)
        runner.set_process('update-user', __cmd_update_user).run()

    @test_flow("app/tests/test-input-data/manager_operation/test_add_datas.json")
    def test_add_datas(self, test_flow: TestCaseFlow):
        """ File/Directory 권한에 따른 저장 """

        def __cmd_upload_file(
                target_user: str, request_user: str,
                file_root: str,
                is_succeed: str, exception_str: str
        ):
            # Test Method: Upload File

            real_file_root: str = self.EXAMPLE_FILES_ROOT + file_root.split('/')[-1]

            # 적용 대상 계정, 요청한 계정
            target_id, request_id = \
                self.change_str_to_static_id(target_user), \
                self.change_str_to_static_id(request_user)

            req = {
                # 요청 데이터
                "static-id": target_id,
                'target-root': file_root,
                'raw-data': read_test_file(real_file_root)
            }

            if is_succeed:
                # 성공 케이스
                self.storage_manager.upload_file(request_id, req, self.user_manager)
                # 업로드 한 후 정상적으로 파일이 저장되어 있는 지 확인
                self.assertTrue(
                    os.path.isfile(
                        os.path.join(self.SYSTEM_ROOT, 'storage', target_id, 'root', file_root)
                    )
                )
            else:
                # 실패 케이스
                try:
                    self.storage_manager.upload_file(request_id, req, self.user_manager)
                except MicrocloudchipException as e:
                    self.assertEqual(type(e).__name__, exception_str)
                else:
                    raise AssertionError("This Case must be failed but it passed or other exception"
                                         f"error case: {req}")

        def __cmd_generate_directory(
                target_user: str, request_user: str,
                dir_root: str,
                is_succeed: str, exception_str: str
        ):
            # 적용 대상 계정, 요청한 계정
            target_id, request_id = \
                self.change_str_to_static_id(target_user), \
                self.change_str_to_static_id(request_user)
            req = {
                'static-id': target_id,
                'target-root': dir_root
            }
            if is_succeed:
                # 성공 케이스
                self.storage_manager.generate_directory(request_id, req)
                # 정상적으로 생성 되었는 지 확인
                self.assertTrue(
                    os.path.isdir(
                        os.path.join(self.SYSTEM_ROOT, 'storage', target_id, 'root', dir_root)
                    )
                )
            else:
                # 실패 케이스
                try:
                    self.storage_manager.generate_directory(request_id, req)
                except MicrocloudchipException as e:
                    self.assertEqual(type(e).__name__, exception_str)
                else:
                    raise AssertionError("This Case must be failed but it passed or other exception"
                                         f"error case: {req}")

        # 테스트 실행
        runner: TestCaseFlowRunner = TestCaseFlowRunner(test_flow)
        runner.set_process('upload-file', __cmd_upload_file) \
            .set_process('generate-dir', __cmd_generate_directory) \
            .run()

    @test_flow("app/tests/test-input-data/manager_operation/test_object_download.json")
    def test_object_download(self, test_flow: TestCaseFlow):
        # 파일 오브젝트 다운로드 테스트

        def __cmd_upload_file(
                target_user: str, request_user: str,
                file_root: str
        ):
            # Test Method: Upload File
            # 해당 모듈 테스트는 이미 위에서 진행했으므로 생략

            real_file_root: str = self.EXAMPLE_FILES_ROOT + file_root.split('/')[-1]

            # 적용 대상 계정, 요청한 계정
            target_id, request_id = \
                self.change_str_to_static_id(target_user), \
                self.change_str_to_static_id(request_user)

            req = {
                # 요청 데이터
                "static-id": target_id,
                'target-root': file_root,
                'raw-data': read_test_file(real_file_root)
            }
            self.storage_manager.upload_file(request_id, req, self.user_manager)

        def __cmd_generate_directory(
                target_user: str, request_user: str,
                dir_root: str,
        ):

            # Test Method: Generate Directory
            # 해당 모듈 테스트는 이미 위에서 진행했으므로 생략

            target_id, request_id = \
                self.change_str_to_static_id(target_user), \
                self.change_str_to_static_id(request_user)
            req = {
                'static-id': target_id,
                'target-root': dir_root
            }
            self.storage_manager.generate_directory(request_id, req)

        def __cmd_download_object(
                target_user: str, request_user: str,
                parent_root: str, objects: list[str],
                is_succeed: bool, exception_str: str
        ):
            # Test Method: Generate Directory
            target_id, request_id = \
                self.change_str_to_static_id(target_user), \
                self.change_str_to_static_id(request_user)

            req = {
                'static-id': target_id,
                'parent-root': parent_root,
                'object-list': objects
            }

            if is_succeed:
                # 성공 케이스
                result_root, _ = self.storage_manager.download_objects(request_id, req)
                # 단일 파일 / 단일 디렉토리 / 다중 파일 x 다중 디렉토리에 따라 다르다
                if len(objects) == 1 and objects[0]['type'] == "file":
                    # 단일 파일일 경우
                    self.assertTrue(os.path.isfile(result_root))
                elif len(objects) == 1 and objects[0]['type'] == "dir":
                    self.assertTrue(os.path.isfile(result_root))
                    os.remove(result_root)
                elif len(objects) > 1:
                    self.assertTrue(os.path.isfile(result_root))
                    os.remove(result_root)

            else:
                # 실패 케이스
                try:
                    self.storage_manager.download_objects(request_id, req)
                except MicrocloudchipException as e:
                    self.assertEqual(type(e).__name__, exception_str)
                else:
                    raise AssertionError("This Case must be failed but it passed or other exception"
                                         f"error case: {req}")

        # 테스트 실행
        runner: TestCaseFlowRunner = TestCaseFlowRunner(test_flow)
        runner.set_process('upload-file', __cmd_upload_file) \
            .set_process('generate-dir', __cmd_generate_directory) \
            .set_process('download-object', __cmd_download_object) \
            .run()

    @test_flow("app/tests/test-input-data/manager_operation/test_update_datas.json")
    def test_update_datas(self, test_flow: TestCaseFlow):
        # 데이터 정보수정 테스트

        def __cmd_upload_file(
                target_user: str, request_user: str,
                file_root: str
        ):
            # Test Method: Upload File
            # 해당 모듈 테스트는 이미 위에서 진행했으므로 생략

            real_file_root: str = self.EXAMPLE_FILES_ROOT + file_root.split('/')[-1]

            # 적용 대상 계정, 요청한 계정
            target_id, request_id = \
                self.change_str_to_static_id(target_user), \
                self.change_str_to_static_id(request_user)

            req = {
                # 요청 데이터
                "static-id": target_id,
                'target-root': file_root,
                'raw-data': read_test_file(real_file_root)
            }
            self.storage_manager.upload_file(request_id, req, self.user_manager)

        def __cmd_generate_directory(
                target_user: str, request_user: str,
                dir_root: str,
        ):
            # Test Method: Generate Directory
            # 해당 모듈 테스트는 이미 위에서 진행했으므로 생략

            target_id, request_id = \
                self.change_str_to_static_id(target_user), \
                self.change_str_to_static_id(request_user)
            req = {
                'static-id': target_id,
                'target-root': dir_root
            }
            self.storage_manager.generate_directory(request_id, req)

        def __cmd_update_file(
                target_user: str, request_user: str,
                target_root: str, new_file_name: str,
                is_succeed: bool, exception_str: str
        ):
            # Test Method: rename filename
            # 적용 대상 계정, 요청한 계정
            target_id, request_id = \
                self.change_str_to_static_id(target_user), \
                self.change_str_to_static_id(request_user)

            req = {
                "static-id": target_id, "target-root": target_root,
                "change": {
                    "name": new_file_name
                }
            }

            if is_succeed:
                self.storage_manager.update_file(request_id, req)
            else:
                try:
                    self.storage_manager.update_file(request_id, req)
                except MicrocloudchipException as e:
                    self.assertEqual(type(e).__name__, exception_str)

        def __cmd_update_directory(
                target_user: str, request_user: str,
                target_root: str, new_dir_name: str,
                is_succeed: bool, exception_str: str
        ):
            # Test Method: rename directory name
            # 적용 대상 계정, 요청한 계정
            target_id, request_id = \
                self.change_str_to_static_id(target_user), \
                self.change_str_to_static_id(request_user)

            req = {
                "static-id": target_id, "target-root": target_root,
                "change": {
                    "name": new_dir_name
                }
            }

            if is_succeed:
                self.storage_manager.update_directory(request_id, req)
            else:
                try:
                    self.storage_manager.update_directory(request_id, req)
                except MicrocloudchipException as e:
                    self.assertEqual(type(e).__name__, exception_str)
                else:
                    raise AssertionError("This Case must be failed but it passed or other exception"
                                         f"error case: {req}")

        # 테스트 코드 실행
        runner: TestCaseFlowRunner = TestCaseFlowRunner(test_flow)
        runner.set_process('upload-file', __cmd_upload_file) \
            .set_process('generate-dir', __cmd_generate_directory) \
            .set_process('update-file', __cmd_update_file) \
            .set_process('update-dir', __cmd_update_directory) \
            .run()

    @test_flow("app/tests/test-input-data/manager_operation/test_get_list_in_directory.json")
    def test_get_list_in_directory(self, test_flow: TestCaseFlow):
        # 디렉토리 에 있는 요소 갖고오기

        def __cmd_upload_file(
                target_user: str, request_user: str,
                file_root: str
        ):
            # Test Method: Upload File
            # 해당 모듈 테스트는 이미 위에서 진행했으므로 생략

            real_file_root: str = self.EXAMPLE_FILES_ROOT + file_root.split('/')[-1]

            # 적용 대상 계정, 요청한 계정
            target_id, request_id = \
                self.change_str_to_static_id(target_user), \
                self.change_str_to_static_id(request_user)

            req = {
                # 요청 데이터
                "static-id": target_id,
                'target-root': file_root,
                'raw-data': read_test_file(real_file_root)
            }
            self.storage_manager.upload_file(request_id, req, self.user_manager)

        def __cmd_generate_directory(
                target_user: str, request_user: str,
                dir_root: str,
        ):
            # Test Method: Generate Directory
            # 해당 모듈 테스트는 이미 위에서 진행했으므로 생략

            target_id, request_id = \
                self.change_str_to_static_id(target_user), \
                self.change_str_to_static_id(request_user)
            req = {
                'static-id': target_id,
                'target-root': dir_root
            }
            self.storage_manager.generate_directory(request_id, req)

        def __cmd_get_directory_information(
                target_user: str, request_user: str,
                dir_root: str,
                is_succeed: bool, exception_str: str,
                expected_file_list: list[str], expected_dir_list: list[str]
        ):
            # Test Method: Get Directory Information
            target_id, request_id = \
                self.change_str_to_static_id(target_user), \
                self.change_str_to_static_id(request_user)

            req = {
                "static-id": target_id,
                "target-root": dir_root
            }

            if is_succeed:
                # 성공 케이스
                f_list, d_list = self.storage_manager.get_dirlist(request_id, req)

                f_list_only_name = [f['file-name'] for f in f_list]
                d_list_only_name = [d['dir-name'] for d in d_list]

                # 검색된 파일 및 디렉토리가 제대로 맞는지 확인
                self.assertListEqual(sorted(expected_file_list), sorted(f_list_only_name))
                self.assertListEqual(sorted(expected_dir_list), sorted(d_list_only_name))

            else:
                try:
                    self.storage_manager.get_dirlist(request_id, req)
                except MicrocloudchipException as e:
                    self.assertEqual(type(e).__name__, exception_str)
                else:
                    raise AssertionError("This Case must be failed but it passed or other exception"
                                         f"error case: {req}")

        # 테스트 솔루션 실행
        runner: TestCaseFlowRunner = TestCaseFlowRunner(test_flow)
        runner.set_process('upload-file', __cmd_upload_file) \
            .set_process('generate-dir', __cmd_generate_directory) \
            .set_process('get-dir-info', __cmd_get_directory_information) \
            .run()

    @test_flow("app/tests/test-input-data/manager_operation/test_delete_datas.json")
    def test_delete_datas(self, test_flow: TestCaseFlow):

        """ Info: Raw 단계와는 달리 Manager 단위에서는 디렉토리를 삭제할 때
            Recursive 하게 삭제합니다.
        """

        def __cmd_upload_file(
                target_user: str, request_user: str,
                file_root: str
        ):
            # Test Method: Upload File
            # 해당 모듈 테스트는 이미 위에서 진행했으므로 생략

            real_file_root: str = self.EXAMPLE_FILES_ROOT + file_root.split('/')[-1]

            # 적용 대상 계정, 요청한 계정
            target_id, request_id = \
                self.change_str_to_static_id(target_user), \
                self.change_str_to_static_id(request_user)

            req = {
                # 요청 데이터
                "static-id": target_id,
                'target-root': file_root,
                'raw-data': read_test_file(real_file_root)
            }
            self.storage_manager.upload_file(request_id, req, self.user_manager)

        def __cmd_generate_directory(
                target_user: str, request_user: str,
                dir_root: str,
        ):
            # Test Method: Generate Directory
            # 해당 모듈 테스트는 이미 위에서 진행했으므로 생략

            target_id, request_id = \
                self.change_str_to_static_id(target_user), \
                self.change_str_to_static_id(request_user)
            req = {
                'static-id': target_id,
                'target-root': dir_root
            }
            self.storage_manager.generate_directory(request_id, req)

        def __cmd_get_directory_information(
                target_user: str, request_user: str,
                dir_root: str,
                expected_file_list: list[str], expected_dir_list: list[str]
        ):
            # Test Method: Get Directory Information
            target_id, request_id = \
                self.change_str_to_static_id(target_user), \
                self.change_str_to_static_id(request_user)

            req = {
                "static-id": target_id,
                "target-root": dir_root
            }

            f_list, d_list = self.storage_manager.get_dirlist(request_id, req)
            f_list_only_name = [f['file-name'] for f in f_list]
            d_list_only_name = [d['dir-name'] for d in d_list]

            # 검색된 파일 및 디렉토리가 제대로 맞는지 확인
            self.assertListEqual(sorted(expected_file_list), sorted(f_list_only_name))
            self.assertListEqual(sorted(expected_dir_list), sorted(d_list_only_name))

        def __cmd_remove(
                mode: str,
                target_user: str, request_user: str,
                target_root: str,
                is_succeed: bool, exception_str: str
        ):
            # Test Method: Get Directory Information
            target_id, request_id = \
                self.change_str_to_static_id(target_user), \
                self.change_str_to_static_id(request_user)

            req = {
                'static-id': target_id,
                'target-root': target_root
            }

            if is_succeed:
                if mode == 'file':
                    self.storage_manager.delete_file(request_id, req)
                elif mode == 'dir':
                    self.storage_manager.delete_directory(request_id, req)
            else:
                try:
                    if mode == 'file':
                        self.storage_manager.delete_file(request_id, req)
                    elif mode == 'dir':
                        self.storage_manager.delete_directory(request_id, req)
                except MicrocloudchipException as e:
                    self.assertEqual(type(e).__name__, exception_str)
                else:
                    raise AssertionError("This Case must be failed but it passed or other exception"
                                         f"error case: {req}")

        TestCaseFlowRunner(test_flow) \
            .set_process('upload-file', __cmd_upload_file) \
            .set_process('generate-dir', __cmd_generate_directory) \
            .set_process('get-dir-info', __cmd_get_directory_information) \
            .set_process('remove', __cmd_remove) \
            .run()

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
            dir_format['target-root'] = f'test-dir/{d}'
            self.storage_manager.generate_directory(self.admin_static_id, dir_format)

        # 파일 하나 생성
        ex_filename: str = self.TEST_FILES[0]
        raw: bytes = read_test_file(os.path.join(self.TEST_FILE_ROOT, ex_filename))

        file_format: dict = {
            "static-id": self.admin_static_id,
            "target-root": f'test-dir/{ex_filename}',
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

        # 삭제 확인
        self.assertFalse(os.path.isdir(os.path.join(self.config.get_system_root(), 'storage', self.other_static_id)))
        self.assertRaises(model.User.DoesNotExist, lambda: model.User.objects.get(static_id=self.other_static_id))
