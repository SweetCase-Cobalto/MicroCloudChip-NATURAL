import json
from app.tests.test_modules.loader import test_flow, TestCaseFlow

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

    def test_make_new_directory(self):

        # 디렉토리 생성 테스트
        input_test_file: str = \
            "app/tests/test-input-data/test_file_dir_control/test_make_new_directory.json"
        test_case = []
        # Test case가 들어있는 파일 부럴오기
        with open(input_test_file, "r") as _f:
            raw = json.load(_f)["test-case"]
            for e in raw:
                test_case.append([
                    e['filename'],
                    e['output'],
                    e['exception']
                ])

        for i in range(len(test_case)):
            # 테스트 시작
            req, pre_result, exception_str = test_case[i]
            test_req_data = {
                "static-id": model.User.objects.get(name="admin").static_id,
                "system-root": self.system_config.get_system_root(),
                "target-root": req,
            }
            if not pre_result:
                # 실패 케이슨

                is_success = True
                # is_success 는 실패/성공 여부
                # Exception 발생 시 False로 전환
                # 따라서 True가 나오면 안됨

                try:
                    # 디렉토리 생성 테스트
                    test_make_directory(test_req_data)
                except MicrocloudchipException as e:
                    # 에러 발생
                    is_success = False
                    # Error Type 맞는 지 검사
                    self.assertEqual(type(e).__name__, exception_str)
                self.assertFalse(is_success)

                if exception_str != MicrocloudchipDirectoryAlreadyExistError.__name__:
                    # 중복 생성 에러가 아니면 디렉토리가 존재하지 않아야 한다.
                    self.assertFalse(os.path.isdir(f"{self.cur_root}{self.token}{req}"))
            else:
                # 성공
                test_make_directory(test_req_data)
                # 디렉토리가 존재해야 한다.
                self.assertTrue(os.path.isdir(f"{self.cur_root}{self.token}{req}"))

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

        while not test_flow.is_empty():
            # start test

            # Test Case 갖고오기
            case = test_flow()
            command, case = case[0], case[1:]

            # 파일 추가일 경우
            if command == 'file':
                filename, root, is_success, exception_str = case
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

            elif command == "dir":
                # 디렉토리 생성은 위에 이미 했기 때문에 성공 케이스만 만든다
                new_dir_root = case[0]
                req = {
                    "static-id": author_static_id,
                    "system-root": self.system_config.get_system_root(),
                    "target-root": new_dir_root
                }
                test_make_directory(req)

    @test_flow("app/tests/test-input-data/test_file_dir_control/test_get_information_of_file.json")
    def test_get_information_of_file(self, test_flow: TestCaseFlow):

        author_static_id = model.User.objects.get(name="admin").static_id

        while not test_flow.is_empty():
            case = test_flow()
            command, case = case[0], case[1:]

            if command == "upload":
                # 파일 정보 체크 테스트를 위한 우선 저장
                filename = case[0]
                binary_data = self.get_raw_data_from_file(f'{self.test_file_root}/{filename}')
                req = {
                    'static-id': author_static_id,
                    'target-root': filename,
                    'system-root': self.system_config.get_system_root(),
                    'raw-data': binary_data
                }
                self.assertTrue(test_upload_file_routine(req))
            elif command == "get":
                filename, is_succeed, expected_file_type, exception = case
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
                        self.assertEqual(type(e).__name__, exception)

    @test_flow("app/tests/test-input-data/test_file_dir_control/test_remove_file.json")
    def test_remove_file(self, test_flow: TestCaseFlow):
        # 파일 삭제
        author_static_id = model.User.objects.get(name="admin").static_id

        while not test_flow.is_empty():
            case = test_flow()
            command, case = case[0], case[1:]

            if command == "file":
                # 파일 정보 체크 테스트를 위한 우선 저장
                filename, root = case
                binary_data = self.get_raw_data_from_file(f'{self.test_file_root}/{filename}')
                req = {
                    'static-id': author_static_id,
                    'target-root': f'{root}{filename}',
                    'system-root': self.system_config.get_system_root(),
                    'raw-data': binary_data
                }
                self.assertTrue(test_upload_file_routine(req))
            elif command == "dir":
                dirname, root = case
                req = {
                    'static-id': author_static_id,
                    'system-root': self.system_config.get_system_root(),
                    'target-root': f'{root}{dirname}'
                }
                test_make_directory(req)
            elif command == "remove":
                file_root, is_succeed, exception = case
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

    def test_modify_file(self):
        # 파일 수정
        """
            다음을 테스트 한다
            1. 정상적으로 파일 수정
            2. 같은 상태로 파일 수정 불가
            3. 삭제된 파일 또는 존재하지 않는 파일 수정 불가
        """

        # 테스트용 파일 생성
        test_files = os.listdir(self.test_file_root)
        author_static_id = model.User.objects.get(name="admin").static_id

        def success_case():
            # 성공 케이스
            raw_data = self.get_raw_data_from_file(self.test_file_root + self.token + test_files[0])
            file_add_req = {
                "static-id": author_static_id,
                "target-root": test_files[0],
                "system-root": self.system_config.get_system_root(),
                "raw-data": raw_data
            }
            # 일단 파일 생성
            test_upload_file_routine(file_add_req)

            # 파일 데이터 갖고오기
            del file_add_req['raw-data']
            file_add_req['root-token'] = self.token
            f = test_get_file_information(file_add_req)

            new_file_name = f"new.{test_files[0].split('.')[-1]}"
            f.update_name(new_file_name)
            self.assertEqual(os.path.isfile(f['full-root']), True)

            # 같은 상태로 파일 수정 불가
            self.assertRaises(MicrocloudchipSystemAbnormalAccessError, lambda: f.update_name(new_file_name))

        def failed_case_removed_file_does_not_modify_name():
            # 실패 케이스: 삭제된 파일은 생성 불능
            raw_data = self.get_raw_data_from_file(self.test_file_root + self.token + test_files[1])
            file_name = test_files[1]
            file_add_req = {
                "static-id": author_static_id,
                "target-root": file_name,
                "system-root": self.system_config.get_system_root(),
                "raw-data": raw_data
            }
            # 파일 생성
            test_upload_file_routine(file_add_req)

            # 파일 데이터 갖고오기
            del file_add_req['raw-data']
            file_add_req['root-token'] = self.token
            f1 = test_get_file_information(file_add_req)
            f2 = test_get_file_information(file_add_req)

            # 파일 삭제
            test_remove_file_routine(f1)
            # 파일 수정 시도 그러나 에러 발생
            self.assertRaises(MicrocloudchipFileNotFoundError, lambda: f2.update_name("mine.mid"))

        success_case()
        failed_case_removed_file_does_not_modify_name()

    def test_get_directory_info(self):
        # 1. Root 단계에서 데이터 구하기

        test_files = os.listdir(self.test_file_root)
        author_static_id = model.User.objects.get(name="admin").static_id
        system_root = self.system_config.get_system_root()

        # 파일 생성
        for test_file in test_files:
            raw_data = self.get_raw_data_from_file(self.test_file_root + self.token + test_file)
            req = {
                'static-id': author_static_id,
                'system-root': system_root,
                'target-root': test_file,
                'raw-data': raw_data
            }
            test_upload_file_routine(req)

        # Root 범위의 디렉토리 데이터 갖고오기
        req = {
            'static-id': author_static_id,
            'system-root': system_root,
            'target-root': '',
            'root-token': self.token
        }
        d = test_get_directory_info_routine(req)

        # 파일 갯수 확인
        self.assertEqual(d['file-size'], len(test_files))

    def test_modify_directory_name(self):

        author_static_id = model.User.objects.get(name="admin").static_id
        system_root = self.system_config.get_system_root()
        req = {
            "static-id": author_static_id,
            "system-root": system_root,
            "target-root": "my-dir"
        }
        test_make_directory(req)
        req['root-token'] = self.token
        d = test_get_directory_info_routine(req)

        # 디렉토리 수정
        d.update_name("other-dir")

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
