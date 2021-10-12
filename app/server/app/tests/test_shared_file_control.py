import os

from django.test import TestCase

from app.tests.test_modules.loader import test_flow, TestCaseFlow, TestCaseFlowRunner
from module.MicrocloudchipException.exceptions import *
from module.data.shared_storage_data import SharedFileData
from module.data.storage_data import FileData
from module.data_builder.shared_storage_builder import SharedFileBuilder
from module.data_builder.user_builder import UserBuilder
from module.manager.internal_database_concurrency_manager import InternalDatabaseConcurrencyManager
from module.specification.System_config import SystemConfig

import app.models as model

TEST_ROOT: str = "app/tests/test-input-data/shared_file_control/"


class SharedFileControlUnittest(TestCase):
    """
    --- 파일 공유 테스트 ---
    0. 파일 및 디렉토리 생성
    1. 파일 공유 설정
        1.1 존재하지 않는 파일 공유 시도 - 에러
        1.2 디렉토리 공유 시도 - 에러
        1.3 정상적인 파일 공유 시도
            1.3.1. 최상위 루트에 있는 파일 공유
            1.3.2. 하위 루트에 있는 파일 공유
        1.4 중복 에러
    2. 파일 공유 데이터 불러오기
        2.1 존재하지 않는 파일 공유 데이터 불러오기 - 에러
        2.2 존재하는 파일이지만 공유 등록이 되어 있지 않은 데이터 불러오기
        2.3 파일 공유 데이터 불러오기
        2.4 공유되었는데 없어진 경우(깜빡하고 삭제가 되었는데 등록해제 안되어 있는 경우)
            info: 파일 삭제에 대한 자동공유 해제는 Manager단에서 운영
    4. 공유 해제
        4.1. 올바른 공유 해제
        4.2. 존재하지 않은 공유 해제
        
    Info:
        Builder, Data Class는 다른 클래스의 상태를 변화해선 안된다.
        그렇기 때문에 다음과 같은 경우는 테스트를 하지 않는다.
        
        1. 파일 및 디렉토리의 이름이 변경되거나 경로의 일부분이 변경되는 경우
        2. 파일 및 상위 디렉토리가 삭제되는 경우
        3. 공유 기한과 관련된 기능
    """
    SYSTEM_CONFIG: SystemConfig = SystemConfig("server/config.json")
    STORAGE_ROOT: str = os.path.join(SYSTEM_CONFIG.get_system_root(), "storage")

    # __methods
    def __add_user(self, is_admin: bool, name: str, email: str) -> str:
        # 가상의 User 생성
        u = UserBuilder()
        u \
            .set_name(name) \
            .set_email(email) \
            .set_is_admin(is_admin) \
            .set_password("12345678") \
            .set_volume_type("TEST") \
            .set_static_id() \
            .build().save()

        static_id: str = u.static_id

        user_root = os.path.join(self.STORAGE_ROOT, static_id)
        os.mkdir(user_root)
        os.mkdir(os.path.join(user_root, "root"))

    def __get_real_root(self, static_id: str, root: str):
        # 실제 루트 생성
        return os.path.join(self.SYSTEM_CONFIG.get_system_root(),
                            "storage", static_id, "root", root)

    @staticmethod
    @InternalDatabaseConcurrencyManager(SystemConfig()).manage_internal_transaction
    def __get_user_id_for_test(user_name):
        # 유저 이름에 대한 아이디
        return model.User.objects.get(name=user_name).static_id

    def __add_file(self, target_user: str, file_root: str, text: str):
        # 파일 추가
        text: bytes = bytes(text, encoding="utf-8")
        static_id: str = self.__get_user_id_for_test(target_user)

        from module.data_builder.file_builder import FileBuilder
        file_builder = FileBuilder()
        file_builder.set_system_root(SystemConfig().get_system_root()) \
            .set_author_static_id(static_id) \
            .set_target_root(file_root) \
            .set_raw_data(text).save()

    def __add_directory(self, target_user: str, dir_root: str):
        # 디렉토리 추가
        static_id: str = self.__get_user_id_for_test(target_user)
        from module.data_builder.directory_builder import DirectoryBuilder
        directory_builder: DirectoryBuilder = DirectoryBuilder()
        directory_builder.set_system_root(SystemConfig().get_system_root()) \
            .set_target_root(dir_root) \
            .set_author_static_id(static_id) \
            .set_target_root(dir_root).save()

    def __remove_file(self, target_user: str, target_root: str):
        # 파일 삭제
        static_id: str = self.__get_user_id_for_test(target_user)
        full_root: str = self.__get_real_root(static_id, target_root)

        file_data: FileData = FileData(full_root)()
        file_data.remove()

    # Share Method
    def __share_file(self, target_user: str, target_root: str,
                     is_succeed: bool, exception_str: str):
        static_id: str = self.__get_user_id_for_test(target_user)

        req_data = {
            "target-user": target_user,
            "target-root": target_root,
            "expected-exception": exception_str
        }
        try:
            SharedFileBuilder() \
                .set_system_root(self.SYSTEM_CONFIG.get_system_root()) \
                .set_author_static_id(static_id) \
                .set_target_root(target_root).save()
        except MicrocloudchipException as e:
            self.assertFalse(is_succeed, msg=f"ERR: This Case is Failed: {req_data}")
            self.assertEqual(type(e).__name__, exception_str)
            return
        except Exception as e:
            # Got Other Exception
            err_msg = f"ERR: Get Python Internal Error: {e}\n req: {req_data}"
            raise AssertionError(err_msg)
        else:
            # Passed
            self.assertTrue(is_succeed, msg=f"ERR: This Case is passed: req: {req_data}")

    def __get_shared_file(self, target_user: str, target_root: str,
                          is_succeed: bool, exception_str: str,
                          expected_file_data: str):

        # 공유된 파일 데이터 불러오기
        static_id: str = self.__get_user_id_for_test(target_user)
        full_root: str = self.__get_real_root(static_id, target_root)

        is_shared: bool = False

        # Search Shared File
        try:
            SharedFileData(self.SYSTEM_CONFIG.get_system_root(), static_id, target_root)()
        except MicrocloudchipFileIsNotSharedError as e:
            # 등록되지 않음 -> 실패
            self.assertFalse(is_succeed, msg=f"{[target_user, target_root, exception_str]}")
        else:
            is_shared = True

        try:
            # Get File Data first
            FileData(full_root)()
        except MicrocloudchipException as e:
            # File Not Exist -> Failed
            self.assertFalse(is_succeed)
            if is_shared:
                self.assertEqual(MicrocloudchipFileSharedButRemovedError.__name__, exception_str)

                # Remove Shared File Database

                InternalDatabaseConcurrencyManager(SystemConfig()).lock_db_process()
                model.SharedFile.objects \
                    .filter(user_static_id=static_id) \
                    .get(file_root=target_root) \
                    .delete()
                InternalDatabaseConcurrencyManager(SystemConfig()).unlock_db_process()
            else:
                self.assertEqual(MicrocloudchipFileNotFoundError.__name__, exception_str)

        else:
            # File Exist
            if not is_shared:
                # But is not shared
                self.assertFalse(is_succeed)
                self.assertEqual(MicrocloudchipFileIsNotSharedError.__name__, exception_str)
            else:
                self.assertTrue(is_succeed, msg=f"Failed: {target_root}")

                # Check Data is Equal
                expected_data_to_byte: bytes = bytes(expected_file_data, encoding='utf-8')
                r: bytes = b""

                # Read from target file
                with open(full_root, 'rb') as f:
                    r += f.read()
                self.assertEqual(r, expected_data_to_byte, msg=f"Result Data Not Equal: {target_user}/{target_root}")

    def __unshare_file(self, target_user: str, target_root: str,
                       is_succeed: bool, exception_str: str):

        static_id: str = self.__get_user_id_for_test(target_user)

        try:
            sf: SharedFileData = SharedFileData(self.SYSTEM_CONFIG.get_system_root(), static_id, target_root)()
        except MicrocloudchipException as e:
            self.assertFalse(is_succeed)
            self.assertEqual(type(e).__name__, exception_str)
        else:
            sf.unshare()

    # Test FUNCTIONS
    @test_flow(f"{TEST_ROOT}/make_shared.json")
    def test_make_shared(self, test_flow: TestCaseFlow):
        # 공유 등록 함수

        TestCaseFlowRunner(test_flow) \
            .set_process("add-user", self.__add_user) \
            .set_process("add-file", self.__add_file) \
            .set_process("add-directory", self.__add_directory) \
            .set_process("share-file", self.__share_file) \
            .run()

    @test_flow(f"{TEST_ROOT}/get_shared_file_data.json")
    def test_get_shared_file_data(self, test_flow: TestCaseFlow):
        # 공유된 파일 데이터 불러오기
        TestCaseFlowRunner(test_flow) \
            .set_process("add-user", self.__add_user) \
            .set_process("add-file", self.__add_file) \
            .set_process("add-directory", self.__add_directory) \
            .set_process("share-file", self.__share_file) \
            .set_process("remove-file", self.__remove_file) \
            .set_process("get-shared-file", self.__get_shared_file) \
            .run()

    @test_flow(f"{TEST_ROOT}/remove_shared_file.json")
    def test_remove_shared_file(self, test_flow: TestCaseFlow):
        # 공유된 파일 해제
        TestCaseFlowRunner(test_flow) \
            .set_process("add-user", self.__add_user) \
            .set_process("add-file", self.__add_file) \
            .set_process("add-directory", self.__add_directory) \
            .set_process("share-file", self.__share_file) \
            .set_process("unshare-file", self.__unshare_file) \
            .run()
