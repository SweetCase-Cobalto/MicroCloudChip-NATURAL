import datetime
import app.models as model
import time

from django.test import TestCase

from app.tests.test_modules.loader import *
from module.data_builder.user_builder import UserBuilder
from module.manager.share_manager import ShareManager
from module.manager.storage_manager import StorageManager
from module.manager.user_manager import UserManager
from module.specification.System_config import SystemConfig

from module.MicrocloudchipException.exceptions import *


class SharedFileManagerUnittest(TestCase):
    """파일 공유 매니저 테스트
        1. 파일 공유 설정
            1.1 존재하지 않은 파일 공유 시도
            1.2 디렉토리 공유 시도
            1.3 정상적인 공유 시도
        2. 파일 공유 데이터 불러오기
            2.1 존재하지 않는 파일 공유 데이터 불러오기 - 에러
            2.2 존재하는 파일이지만 공유 등록이 되어 있지 않은 데이터 불러오기
            2.3 파일 공유 데이터 불러오기
        3. 공유 해제
            3.1 존재하지 않은 공유 해제
            3.2 정상적인 공유 해제
        4 공유 대상 파일이 삭제된 경우, Shared Db도 같이 삭제되는지 확인
        5 상위 디렉토리가 삭제된 경우, Shared DB도 같이 삭제되는 지 확인
        6.디렉토리 및 파일의 이름이 바뀔 경우, Shared Data도 변경이 일어나는 지 확인
    """
    SYSTEM_CONFIG: SystemConfig = SystemConfig("server/config.json")
    TEST_FILE_ROOT: str = "app/tests/test-input-data/shared_manager/"

    USER_MANAGER: UserManager = None
    STORAGE_MANAGER: StorageManager = None
    SHARE_MANAGER: ShareManager = None

    # Sub Functions
    def __add_admin_user(self, name: str, email: str):
        u = UserBuilder()
        u \
            .set_name(name) \
            .set_is_admin(True) \
            .set_email(email) \
            .set_password("12345678") \
            .set_volume_type("TEST") \
            .set_static_id() \
            .build().save()

    def __change_name_to_id(self, name: str):
        return model.User.objects.get(name=name).static_id

    def __str_to_byte(self, text: str) -> bytes:
        return bytes(text, encoding='utf-8')

    # Test Functions
    def __cmd_add_user(self, name: str, email: str):
        # Test Method: Add User
        static_id: str = self.__change_name_to_id("admin")
        self.USER_MANAGER.add_user(static_id, {
            "name": name, "password": "12345678",
            "email": email, "volume-type": "TEST",
            "img-raw-data": None, "img-extension": None
        })

    def __cmd_add_file(self, target_user: str, file_root: str, text: str):
        # Test Method: Add File
        static_id: str = self.__change_name_to_id(target_user)
        admin_static_id: str = self.__change_name_to_id("admin")
        text_to_byte = bytes(text, encoding="utf-8")

        self.STORAGE_MANAGER.upload_file(admin_static_id, {
            "static-id": static_id,
            "target-root": file_root,
            "raw-data": text_to_byte
        }, self.USER_MANAGER)

    def __cmd_generate_directory(self, target_user: str, dir_root: str):
        # Test Method: Generate Directory
        static_id: str = self.__change_name_to_id(target_user)
        admin_static_id: str = self.__change_name_to_id("admin")

        self.STORAGE_MANAGER.generate_directory(admin_static_id, {
            "static-id": static_id, 'target-root': dir_root
        })

    def __cmd_share_file(self, target_user: str, file_root: str,
                         is_succeed: bool, exception_str: str):
        # Test Method: Share File
        static_id: str = self.__change_name_to_id(target_user)
        admin_static_id: str = self.__change_name_to_id("admin")

        log = [target_user, file_root, is_succeed, exception_str]

        try:
            # 파일 공유 시도
            self.SHARE_MANAGER.share_file(admin_static_id, static_id,
                                          file_root)
        except MicrocloudchipException as e:
            # 실패
            self.assertFalse(is_succeed, msg=f"This case must be passed but got error: {log}")
            self.assertEqual(type(e).__name__, exception_str, msg=f"Other exception occured: {log}")
        except Exception as e:
            # Other Exception
            # Get Error
            raise AssertionError(f"Other Exception Occured: {log}: {type(e).__name__}: {e}")
        else:
            self.assertTrue(is_succeed, msg=f"This case must be failed but passed: {log}")

    def __cmd_get_shared_data(self, target_user: str, file_root: str,
                              is_succeed: bool, exception_str: str, expected_file_data: str):

        # Test Method: Get Shared Data(real root)
        static_id: str = self.__change_name_to_id(target_user)
        log = [target_user, file_root, is_succeed, exception_str, expected_file_data]
        try:
            shared_id: str = self.SHARE_MANAGER.get_shared_id(static_id, file_root)
            real_root: str = self.SHARE_MANAGER.download_shared_file(shared_id)

            # get data
            rd: bytes = b''
            with open(real_root, 'rb') as _f:
                rd += _f.read()

        except MicrocloudchipException as e:
            self.assertFalse(is_succeed, msg=f"This case must be passed but got error: {log}, {e}")
            self.assertEqual(type(e).__name__, exception_str, msg=f"Other exception occured: {log}")
        except Exception as e:
            # Other Exception
            # Get Error
            raise AssertionError(f"Other Exception Occured: {log}: {type(e).__name__}: {e}")
        else:
            self.assertEqual(rd, self.__str_to_byte(expected_file_data), msg=f"result data not correct: {log}")
            self.assertTrue(is_succeed, msg=f"This case must be failed but passed: {log}")

    def __cmd_get_shared_data_after_expired(self, target_user: str, file_root: str,
                                            is_succeed: bool, exception_str: str):
        # Test Method: 만료된 Shared Data 뽑아오기

        # 1 microseconds로 줄이기
        time.sleep(0.2)
        self.__cmd_get_shared_data(target_user, file_root, is_succeed, exception_str, None)

    def __cmd_remove_file(self, target_user: str, file_root: str):
        # Test Method: Remove File
        admin_static_id: str = self.__change_name_to_id("admin")
        static_id: str = self.__change_name_to_id(target_user)

        self.STORAGE_MANAGER.delete_file(admin_static_id, {
            "static-id": static_id, "target-root": file_root
        }, self.SHARE_MANAGER)

    def __cmd_unshare_file(self, target_user: str, file_root: str, is_succeed: bool, exception_str: str):

        log = [target_user, file_root, is_succeed, exception_str]

        # Test Method: unshare file
        admin_static_id: str = self.__change_name_to_id("admin")
        static_id: str = self.__change_name_to_id(target_user)
        shared_id: str = self.SHARE_MANAGER.get_shared_id(static_id, file_root)

        try:
            self.SHARE_MANAGER.unshare_file(admin_static_id, static_id, shared_id)
        except MicrocloudchipException as e:
            self.assertFalse(is_succeed, msg=f"This case must be passed but failed: {log}:{e}")
        except Exception as e:
            raise AssertionError(f"Uknown Exception occur: {str(e)}")

    def __cmd_remove_directory(self, target_user: str, dir_root: str):

        admin_static_id: str = self.__change_name_to_id("admin")
        static_id: str = self.__change_name_to_id(target_user)

        self.STORAGE_MANAGER.delete_directory(admin_static_id, {
            "static-id": static_id, "target-root": dir_root
        }, self.SHARE_MANAGER)

    def __cmd_update_file_name(self, target_user: str, file_root: str, new_name: str):

        admin_static_id: str = self.__change_name_to_id("admin")
        static_id: str = self.__change_name_to_id(target_user)

        req = {
            "static-id": static_id, "target-root": file_root,
            "change": {
                "name": new_name
            }
        }
        self.STORAGE_MANAGER.update_file(admin_static_id, req, self.SHARE_MANAGER)

    def __cmd_update_directory(self, target_user: str, dir_root: str, new_dir_name: str):

        admin_static_id: str = self.__change_name_to_id("admin")
        static_id: str = self.__change_name_to_id(target_user)

        req = {
            "static-id": static_id, "target-root": dir_root,
            "change": {
                "name": new_dir_name
            }
        }
        self.STORAGE_MANAGER.update_directory(admin_static_id, req, self.SHARE_MANAGER)

    # Run Functions
    def setUp(self) -> None:
        # 매니저 생성
        self.USER_MANAGER = UserManager(self.SYSTEM_CONFIG)
        self.STORAGE_MANAGER = StorageManager(self.SYSTEM_CONFIG)
        self.SHARE_MANAGER = \
            ShareManager(self.SYSTEM_CONFIG, datetime.timedelta(days=30))

    @test_flow(f"{TEST_FILE_ROOT}share_file.json")
    def test_share_file(self, test_flow: TestCaseFlow):
        # 파일 공유 테스트
        TestCaseFlowRunner(test_flow) \
            .set_process('add-user', self.__cmd_add_user) \
            .set_process('add-file', self.__cmd_add_file) \
            .set_process('share-file', self.__cmd_share_file) \
            .set_process('add-directory', self.__cmd_generate_directory) \
            .run()

    @test_flow(f"{TEST_FILE_ROOT}get_share_data.json")
    def test_get_share_data(self, test_flow: TestCaseFlow):

        # 공유 데이터 파일 얻기 테스트
        TestCaseFlowRunner(test_flow) \
            .set_process('add-user', self.__cmd_add_user) \
            .set_process('add-file', self.__cmd_add_file) \
            .set_process('share-file', self.__cmd_share_file) \
            .set_process('add-directory', self.__cmd_generate_directory) \
            .set_process('get-shared-file', self.__cmd_get_shared_data) \
            .run()

    @test_flow(f"{TEST_FILE_ROOT}unshare_file.json")
    def test_unshare_file(self, test_flow: TestCaseFlow):
        #  공유 해제
        TestCaseFlowRunner(test_flow) \
            .set_process('add-file', self.__cmd_add_file) \
            .set_process('share-file', self.__cmd_share_file) \
            .set_process('add-directory', self.__cmd_generate_directory) \
            .set_process("unshare-file", self.__cmd_unshare_file) \
            .run()

    @test_flow(f"{TEST_FILE_ROOT}auto_unshare_when_file_removed.json")
    def test_auto_unshare_when_file_removed(self, test_flow: TestCaseFlow):
        # 공유된 파일이 삭제되면 공유된 내용도 삭제되어야 한다.

        #  공유 해제
        TestCaseFlowRunner(test_flow) \
            .set_process('add-file', self.__cmd_add_file) \
            .set_process('share-file', self.__cmd_share_file) \
            .set_process('add-directory', self.__cmd_generate_directory) \
            .set_process('remove-file', self.__cmd_remove_file) \
            .set_process('get-shared-file', self.__cmd_get_shared_data) \
            .run()

    @test_flow(f"{TEST_FILE_ROOT}auto_unshare_when_directory_removed.json")
    def test_auto_unshare_when_directory_removed(self, test_flow: TestCaseFlow):
        # 디렉토리가 삭제되면 그 안의 공유된 파일들도 삭제되어야 한다.
        TestCaseFlowRunner(test_flow) \
            .set_process('add-file', self.__cmd_add_file) \
            .set_process('share-file', self.__cmd_share_file) \
            .set_process('add-directory', self.__cmd_generate_directory) \
            .set_process('get-shared-file', self.__cmd_get_shared_data) \
            .set_process("remove-dir", self.__cmd_remove_directory) \
            .run()

    @test_flow(f"{TEST_FILE_ROOT}auto_changed_name_when_file_or_directory_changed.json")
    def test_auto_changed_name_when_file_or_directory_changed(self, test_flow: TestCaseFlow):
        # 공유 데이터 파일 얻기 테스트

        TestCaseFlowRunner(test_flow) \
            .set_process('add-user', self.__cmd_add_user) \
            .set_process('add-file', self.__cmd_add_file) \
            .set_process('share-file', self.__cmd_share_file) \
            .set_process('add-directory', self.__cmd_generate_directory) \
            .set_process('get-shared-file', self.__cmd_get_shared_data) \
            .set_process('update-file', self.__cmd_update_file_name) \
            .set_process('update-dir', self.__cmd_update_directory) \
            .run()
