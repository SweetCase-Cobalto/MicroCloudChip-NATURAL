from django.test import TestCase

from module.data_builder.user_builder import UserBuilder
from module.specification.System_config import SystemConfig
from module.MicrocloudchipException.exceptions import *
from app.tests.test_modules.testing_file_dir_control_module import *
import app.models as model
import os
import sys


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
        3. 파일 정보 수정 (이름 수정)
        4. 파일 삭제

        -- 디렉토리[정보 갖고오기] --
        1. 디렉토리 정보 갖고오기
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

        # 디랙토리 생성
        test_case = [
            (f"aavvccs{self.token}vkdsfdsd", False, MicrocloudchipDirectoryNotFoundError),
            ("fs:fds:fd", False, MicrocloudchipFileAndDirectoryValidateError),
            ("fs*fds*fd", False, MicrocloudchipFileAndDirectoryValidateError),
            ("fs?fs?fs", False, MicrocloudchipFileAndDirectoryValidateError),
            ("fs>fs>fs", False, MicrocloudchipFileAndDirectoryValidateError),
            ("fs<fs<Fs", False, MicrocloudchipFileAndDirectoryValidateError),
            ('''fs"fs"fs''', False, MicrocloudchipFileAndDirectoryValidateError),
            ("fs|fs|fs", False, MicrocloudchipFileAndDirectoryValidateError),
            ("mydirectory", True, None),
            ("mydirectory", False, MicrocloudchipDirectoryAlreadyExistError),
            (f"mydirectory{self.token}semidirectory", True, None),

            # 운영체제에 따른 실패 케이스 추가
            (f"mydirectory{self.token}aaff///" if self.token == '\\' else f"mydirectory{self.token}aaff\\", False,
             MicrocloudchipFileAndDirectoryValidateError)
        ]

        for i in range(len(test_case)):

            req, pre_result, exception = test_case[i]

            test_req_data = {
                "static-id": model.User.objects.get(name="admin").static_id,
                "system-root": self.system_config.get_system_root(),
                "target-root": req,
            }
            if not pre_result:
                # 실패
                self.assertRaises(exception, lambda: test_make_directory(test_req_data))
                # 디렉토리가 존재해서는 안된다.
                if exception != MicrocloudchipDirectoryAlreadyExistError:
                    # 중복 추가 에러가 아니면 실수로 생성되었는 지 측정한다.
                    self.assertEqual(os.path.isdir(f"{self.cur_root}{self.token}{req}"), False)
            else:
                # 성공
                test_make_directory(test_req_data)
                # 디렉토리가 존재해야 한다.
                self.assertEqual(os.path.isdir(f"{self.cur_root}{self.token}{req}"), True)

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

    def test_upload_file(self):
        # Validate Check 는 Directory 와 동일하기 때문에
        # 업로드 여부, 종복 여부만 체크한다.
        test_files = os.listdir(self.test_file_root)
        author_static_id = model.User.objects.get(name="admin").static_id

        # 테스트 대상
        """
            success: 성공
            success-after-make-directory: 디렉토리 생성 후에 성공
            failed: 실패
        """
        test_case = {
            "success": test_files,
            "success-after-make-directory": f"directory{self.token}{test_files[0]}",
            "failed": f"no{self.token}{test_files[1]}",
        }

        # In Success
        for test_file in test_case['success']:
            binary_data = self.get_raw_data_from_file(self.test_file_root + self.token + test_file)
            # 테스트 돌리기
            req = {
                "static-id": author_static_id,
                "target-root": test_file,
                "system-root": self.system_config.get_system_root(),
                "raw-data": binary_data
            }
            # 업로드와 동시에 정상적으로 추가되었는 지 확인
            self.assertEqual(test_upload_file(req), True)

        # 디렉토리 생성
        dir_req = {
            "static-id": author_static_id,
            "system-root": self.system_config.get_system_root(),
            "target-root": "directory",
        }
        test_make_directory(dir_req)
        
        # 디랙토리 생성 후 성공
        __test_file = test_case['success-after-make-directory']
        __raw_data = self.get_raw_data_from_file(self.test_file_root + self.token + test_files[0])
        file_req = {
            "static-id": author_static_id,
            "target-root": __test_file,
            "system-root": self.system_config.get_system_root(),
            "raw-data": __raw_data
        }
        self.assertEqual(test_upload_file(file_req), True)
        # 중복 추가 불가능
        self.assertRaises(MicrocloudchipFileAlreadyExistError, lambda: test_upload_file(file_req))

        # 실패
        __test_file = test_case['failed']
        __raw_data = self.get_raw_data_from_file(self.test_file_root + self.token + test_files[1])
        file_req['target-root'] = __test_file
        file_req['raw-data'] = __raw_data
        self.assertRaises(MicrocloudchipDirectoryNotFoundError, lambda: test_upload_file(file_req))

    def test_get_information_of_file(self):
        # 파일 관련 정보 갖고오기
        pass

    def test_modify_file_name(self):
        # 파일 이름 바꾸기 테스트
        pass

    def test_get_directory_info_and_file_list(self):
        # 디렉토리 정보와 파일 조회하기
        pass

    def test_remove_directory_recursive(self):
        # 디렉토리 순환 삭제
        pass
