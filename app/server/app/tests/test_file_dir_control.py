import json
from app.tests.test_modules.loader import test_flow, TestCaseFlow, TestCaseFlowRunner

from django.test import TestCase

import app.models as model
from app.tests.test_modules.testing_file_dir_control_module import *
from module.data_builder.user_builder import UserBuilder
from module.specification.System_config import SystemConfig


class FileDirControlTestUnittest(TestCase):
    """파일 및 디렉토리 raw 단계 운용 테스트"""

    """
        테스트 항목
        
        -- 디렉토리[생성 및 삭제] --
        1. 디렉토리 
        
        --- 파일 ---
        1. 파일 가상 업로드
        2. 파일 정보 갖고오기
            3. 파일 확장자에 따른 파일 타입 구하기
        3. 파일 삭제
        4. 파일 정보 수정 (이름 수정)

        -- 디렉토리[정보 갖고오기] --
        1. 디렉토리 정보 갖고오기
        2. 디렉토리 정보 수정
        2. 디렉토리 recursive 삭제
        
        
        주의
        해당 테스트는 오직 '파일 및 디렉토리' 만 운용하는 테스트를 한다
        공유 등 외의 기능은 manager 단계에서 테스트한다
        
        따라서 테스트 모듈 중 일부는 Manager 기능에 추가 될 것 
        
        테스트 대상 객체
        FileDataBuilder, FileData
        DirectoryDataBuilder, DirectoryData
    """

    # Variables
    CONFIG_FILE_ROOT: str = ["server", "config.json"]
    system_config: SystemConfig = SystemConfig(os.path.join(*CONFIG_FILE_ROOT))

    token: str = '\\' if sys.platform == "win32" else "/"

    # User 저장소
    test_user_root: str = f"{system_config.get_system_root()}{token}storage{token}"
    cur_root: str = ""

    # Test Files Root
    test_file_root: str = "app/tests/test-input-data/example_files"

    def setUp(self) -> None:
        # 파일 테스트를 위한 가상 Admin 생성
        user_builder = UserBuilder()
        user_builder.set_name("admin") \
            .set_email("seokbong60@gmail.com") \
            .set_password("1234567890") \
            .set_is_admin(True) \
            .set_volume_type("TEST") \
            .set_static_id() \
            .build().save()

        # User Root 갱신
        self.test_user_root += user_builder.static_id
        os.mkdir(self.test_user_root)

        # 해당 User 에 대한 파일 및 디렉토리 관리는 root 에서 진행한다.
        self.cur_root = f"{self.test_user_root}{self.token}root"
        os.mkdir(self.cur_root)

        # Check is Directory Exist
        self.assertEqual(os.path.isdir(self.cur_root), True)

    @test_flow("app/tests/test-input-data/test_file_dir_control/test_make_new_directory.json")
    def test_make_new_directory(self, test_flow: TestCaseFlow):

        static_id: str = model.User.objects.get(name="admin").static_id

        def __cmd_generate_dir(filename: str, is_succeed: bool, exception_str: str):
            req = {
                'static-id': static_id,
                'system-root': self.system_config.get_system_root(),
                'target-root': filename
            }
            if is_succeed:
                test_make_directory(req)
                self.assertTrue(os.path.isdir(f"{self.cur_root}{self.token}{filename}"))
            else:
                try:
                    test_make_directory(req)
                except MicrocloudchipException as e:
                    self.assertEqual(type(e).__name__, exception_str)
                    if exception_str != MicrocloudchipDirectoryAlreadyExistError.__name__ and \
                            exception_str != MicrocloudchipFileAndDirectoryNameEmpty.__name__:
                        # 중복 에러나 디렉토리 이름이 비어있는 경우가 아니라면 파일이 존재해선 안된다.
                        self.assertFalse(os.path.isdir(f"{self.cur_root}{self.token}{filename}"))
                else:
                    raise AssertionError(f"It is succeed or other exceptions: {req}")

        runner: TestCaseFlowRunner = TestCaseFlowRunner(test_flow)
        runner.set_process('dir', __cmd_generate_dir).run()

    @staticmethod
    def get_raw_data_from_file(file_root: str) -> bytes:
        raw = b''
        with open(file_root, 'rb') as f:
            while True:
                r = f.readline()
                if not r:
                    break
                raw += r
        return raw

    @test_flow("app/tests/test-input-data/test_file_dir_control/test_upload_file.json")
    def test_upload_file(self, test_flow: TestCaseFlow):
        # Validate Check 는 Directory 와 동일하기 때문에
        # 업로드 여부, 종복 여부만 체크한다.

        # 테스트를 수행 할 static_id 구하기
        author_static_id = model.User.objects.get(name="admin").static_id

        def __cmd_file(filename, root, is_success, exception_str):
            # Test Function: file upload
            __file_root = f'{self.test_file_root}/{filename}'
            if os.path.isfile(__file_root):
                # 실제 존재하는 이미지면 파일 바이너리 데이터 갖고오기
                binary_data = self.get_raw_data_from_file(f'{self.test_file_root}/{filename}')
            else:
                # 없는 경우 임의데이터 생성
                binary_data = bytes("abcdefd", 'utf-8')
            req = {
                'static-id': author_static_id,
                'target-root': root + filename,
                'system-root': self.system_config.get_system_root(),
                "raw-data": binary_data
            }
            if is_success:
                # 성공 케이스
                self.assertTrue(test_upload_file_routine(req))
            else:
                # 실패 케이스
                try:
                    test_upload_file_routine(req)
                except MicrocloudchipException as e:
                    self.assertEqual(exception_str, type(e).__name__)
                else:
                    # 통과하면 안됨
                    # AssertionError 호출
                    raise AssertionError(f"This Case {req} does not occur Error!")

        def __cmd__dir(new_dir_root):
            # Test Function
            # 디렉토리 생성은 위에 이미 했기 때문에 성공 케이스만 만든다
            req = {
                "static-id": author_static_id,
                "system-root": self.system_config.get_system_root(),
                "target-root": new_dir_root
            }
            test_make_directory(req)

        # 테스트 함수 등록 및 돌리기
        test_runner = TestCaseFlowRunner(test_flow)
        test_runner.set_process('file', __cmd_file) \
            .set_process('dir', __cmd__dir) \
            .run()

    @test_flow("app/tests/test-input-data/test_file_dir_control/test_get_information_of_file.json")
    def test_get_information_of_file(self, test_flow: TestCaseFlow):

        author_static_id = model.User.objects.get(name="admin").static_id

        def __cmd_upload_file(filename: str):
            # Test Method: Upload file
            binary_data = self.get_raw_data_from_file(f'{self.test_file_root}/{filename}')
            req = {
                'static-id': author_static_id,
                'target-root': filename,
                'system-root': self.system_config.get_system_root(),
                'raw-data': binary_data
            }
            self.assertTrue(test_upload_file_routine(req))

        def __cmd_get_info(filename: str, is_succeed: bool, expected_file_type: str, exception_str: str):
            req = {
                'static-id': author_static_id,
                'target-root': filename,
                'system-root': self.system_config.get_system_root(),
                'root-token': self.token
            }
            # 성공할 경우
            if is_succeed:
                f = test_get_file_information(req)
                self.assertEqual(f['file-type'].name, expected_file_type)
            else:
                try:
                    test_get_file_information(req)
                except MicrocloudchipException as e:
                    self.assertEqual(type(e).__name__, exception_str)
                else:
                    # 통과하면 안됨
                    # AssertionError 호출
                    raise AssertionError(f"This Case {req} does not occur Error!")

            runner: TestCaseFlowRunner = TestCaseFlowRunner(test_flow)
            runner.set_process('upload', __cmd_upload_file) \
                .set_process('get', __cmd_get_info) \
                .run()

    @test_flow("app/tests/test-input-data/test_file_dir_control/test_remove_file.json")
    def test_remove_file(self, test_flow: TestCaseFlow):
        # 파일 삭제
        author_static_id = model.User.objects.get(name="admin").static_id

        def __cmd_file(filename: str, root: str):
            # Test Method: 파일 저장
            # 파일 정보 체크 테스트를 위한 우선 저장
            binary_data = self.get_raw_data_from_file(f'{self.test_file_root}/{filename}')
            req = {
                'static-id': author_static_id,
                'target-root': f'{root}{filename}',
                'system-root': self.system_config.get_system_root(),
                'raw-data': binary_data
            }
            self.assertTrue(test_upload_file_routine(req))

        def __cmd_dir(dirname: str, root: str):
            # Test Method: 디렉토리 생성
            req = {
                'static-id': author_static_id,
                'system-root': self.system_config.get_system_root(),
                'target-root': f'{root}{dirname}'
            }
            test_make_directory(req)

        def __cmd_remove(file_root: str, is_succeed: bool, exception: MicrocloudchipException):
            # Test Method: 파일 제거
            req = {
                'static-id': author_static_id,
                'target-root': file_root,
                'system-root': self.system_config.get_system_root(),
                'root-token': self.token
            }
            if is_succeed:
                # 성공
                # 파일 데이터 불러오기
                f = test_get_file_information(req)
                # 파일 삭제 시도
                self.assertTrue(test_remove_file_routine(f))
            else:
                try:
                    f = test_get_file_information(req)
                    test_remove_file_routine(f)
                except MicrocloudchipException as e:
                    self.assertEqual(type(e).__name__, exception)
                else:
                    # 통과하면 안됨
                    # AssertionError 호출
                    raise AssertionError(f"This Case {req} does not occur Error!")

        # 테스트 메소드 등록 및 실행
        runner: TestCaseFlowRunner = TestCaseFlowRunner(test_flow)
        runner.set_process('file', __cmd_file) \
            .set_process('dir', __cmd_dir) \
            .set_process('remove', __cmd_remove) \
            .run()

    @test_flow("app/tests/test-input-data/test_file_dir_control/test_modify_file.json")
    def test_modify_file(self, test_flow: TestCaseFlow):
        # 파일 수정
        """
            다음을 테스트 한다
            1. 정상적으로 파일 수정
            2. 같은 상태로 파일 수정 불가
            3. 삭제된 파일 또는 존재하지 않는 파일 수정 불가
        """

        # 테스트용 파일 생성
        author_static_id = model.User.objects.get(name="admin").static_id

        def __cmd_update_file(filename: str, root: str):
            # Test Method: 파일 저장
            # 파일 이름을 변경하려면 일단 파일이 저장되어 있어야 한다.
            binary_data = self.get_raw_data_from_file(f'{self.test_file_root}/{filename}')
            req = {
                'static-id': author_static_id,
                'target-root': f'{root}{filename}',
                'system-root': self.system_config.get_system_root(),
                'raw-data': binary_data
            }
            self.assertTrue(test_upload_file_routine(req))

        def __cmd_modify_file(filename: str, root: str, new_name: str, is_succeed: bool,
                              exception_str: str):
            req = {
                'static-id': author_static_id,
                'target-root': f'{root}{filename}',
                'system-root': self.system_config.get_system_root(),
                'root-token': self.token
            }
            # 파일 데이터 갖고오기
            f: FileData = test_get_file_information(req)

            # 예상 변경된 파일의 전체 루트 구하기
            __expected_full_root_tmp_list = f['full-root'].split(self.token)[:-1] + [new_name]
            expected_full_root = self.token.join(__expected_full_root_tmp_list)

            # 변경 시도
            if is_succeed:
                # 성공해야 하는 케이스
                f.update_name(new_name)
                # full root가 변경된 파일 이름에 의해 같이 바뀌었는 지 확인
                self.assertEqual(expected_full_root, f['full-root'])
                # 파일이 존재하는 지 확인
                self.assertTrue(os.path.isfile(f['full-root']))
            else:
                try:
                    f.update_name(new_name)

                except MicrocloudchipException as e:
                    self.assertEqual(type(e).__name__, exception_str)
                else:
                    # 통과하면 안됨
                    # AssertionError 호출
                    raise AssertionError(f"This Case {req} does not occur Error!")

        # 테스트 메소드 등록 및 실행
        runner: TestCaseFlowRunner = TestCaseFlowRunner(test_flow)
        runner.set_process('file', __cmd_update_file) \
            .set_process('modify', __cmd_modify_file) \
            .run()

    @test_flow("app/tests/test-input-data/test_file_dir_control/test_get_directory_info.json")
    def test_get_directory_info(self, test_flow: TestCase):

        # 1. Root 단계에서 데이터 구하기
        author_static_id = model.User.objects.get(name="admin").static_id

        def __cmd_update_file(filename: str, root: str):
            # Test Method: 파일 저장
            # 파일 이름을 변경하려면 일단 파일이 저장되어 있어야 한다.
            binary_data = self.get_raw_data_from_file(f'{self.test_file_root}/{filename}')
            req = {
                'static-id': author_static_id,
                'target-root': f'{root}{filename}',
                'system-root': self.system_config.get_system_root(),
                'raw-data': binary_data
            }
            self.assertTrue(test_upload_file_routine(req))

        def __cmd_generate_dir(dirname: str, root: str):
            # Test Method: 디렉토리 생성
            req = {
                'static-id': author_static_id,
                'target-root': f'{root}{dirname}',
                'system-root': self.system_config.get_system_root()
            }
            test_make_directory(req)

        def __cmd_get_directory_info(dirname: str, root: str, is_succeed: bool,
                                     expected_file_size: int, exception_str: str):
            # Test Method: 디렉토리 데이터 갖고오기
            req = {
                'static-id': author_static_id,
                'system-root': self.system_config.get_system_root(),
                'target-root': f'{root}{dirname}',
                'root-token': self.token
            }
            if is_succeed:
                d: DirectoryData = test_get_directory_info_routine(req)
                self.assertEqual(d['file-size'], expected_file_size)
            else:
                try:
                    test_get_directory_info_routine(req)
                except MicrocloudchipException as e:
                    self.assertEqual(type(e).__name__, exception_str)
                else:
                    raise AssertionError(f"This Case {req} does not occur Error!")

        runner: TestCaseFlowRunner = TestCaseFlowRunner(test_flow)
        runner.set_process('upload-file', __cmd_update_file) \
            .set_process('generate-dir', __cmd_generate_dir) \
            .set_process('get-directory-info', __cmd_get_directory_info) \
            .run()

    @test_flow("app/tests/test-input-data/test_file_dir_control/test_modify_directory_name.json")
    def test_modify_directory_name(self, test_flow: TestCase):

        author_static_id = model.User.objects.get(name="admin").static_id

        def __cmd_generate_dir(dirname: str, root: str):
            # Test Method: 디렉토리 생성
            req = {
                'static-id': author_static_id,
                'target-root': f'{root}{dirname}',
                'system-root': self.system_config.get_system_root()
            }
            test_make_directory(req)

        def __cmd_update_directory(new_name: str, dirname: str,
                                   root: str, is_succeed: bool, exception_str: str):
            # Test Method: 디렉토리 이름 변경
            req = {
                "static-id": author_static_id,
                "system-root": self.system_config.get_system_root(),
                "target-root": f'{root}{dirname}',
                'root-token': self.token
            }

            try:
                d: DirectoryData = test_get_directory_info_routine(req)
                d.update_name(new_name)
            except MicrocloudchipException as e:
                if is_succeed:
                    # 성공인데 실패하면 에러
                    raise AssertionError(f"This case must be succeed but failed:\n"
                                         f"command: update-directory\n"
                                         f"req: {req}\n"
                                         f"error: {e}")
                else:
                    # 실패
                    self.assertEqual(type(e).__name__, exception_str)
            else:
                if not is_succeed:
                    raise AssertionError(f"This Case {req} does not occur Error!")

        runner: TestCaseFlowRunner = TestCaseFlowRunner(test_flow)
        runner.set_process('generate-dir', __cmd_generate_dir) \
            .set_process('update-dir', __cmd_update_directory) \
            .run()

    def test_remove_directory_recursive(self):

        test_files = os.listdir(self.test_file_root)
        author_static_id = model.User.objects.get(name="admin").static_id
        system_root = self.system_config.get_system_root()
        target_dir = 'dir'

        dir_req = {
            'static-id': author_static_id,
            'system-root': system_root,
            'target-root': target_dir
        }

        test_make_directory(dir_req)

        # 파일 업로드
        for t in test_files:
            target_root = f"{target_dir}/{t}"
            b = self.get_raw_data_from_file(self.test_file_root + self.token + t)
            r = {
                'static-id': author_static_id,
                'system-root': system_root,
                'target-root': target_root,
                'raw-data': b
            }
            self.assertEqual(test_upload_file_routine(r), True)

        # 디렉토리 조회
        dir_req['root-token'] = self.token
        d = test_get_directory_info_routine(dir_req)
        dir_full_root = d['full-root']

        # 삭제
        # 하위 데이터가 있다면 삭제를 할 수 없다.

        self.assertRaises(MicrocloudchipDirectoryDeleteFailedBacauseOfSomeData, lambda: d.remove())

        # 삭제 여부 확인
        # 삭제 되면 안됨
        self.assertTrue(os.path.isdir(dir_full_root))
