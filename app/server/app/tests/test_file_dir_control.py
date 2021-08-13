from django.test import TestCase

from module.data_builder.user_builder import UserBuilder
from module.specification.System_config import SystemConfig
from module.MicrocloudchipException.exceptions import *
import os
import sys


class FileDirControlTestUnittest(TestCase):
    """파일 및 디렉토리 raw 단계 운용 테스트"""

    """
        테스트 항목
        
        -- 디렉토리[생성 및 삭제] --
        1. 디렉토리 생성
        2. 디렉토리 삭제
        
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
        self.cur_root = f"{self.test_user_root}\\root" if sys.platform == "win32" else f"{self.test_user_root}/root"
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
            ("mydirectory", False, MicrocloudchipDirectoryAleadyExistError),
            (f"mydirectory{self.token}semidirectory", True),

            # 운영체제에 따른 실패 케이스 추가
            (f"mydirectory{self.token}aaff///" if self.token == '\\' else f"mydirectory{self.token}aaff\\", False,
             MicrocloudchipFileAndDirectoryValidateError)
        ]

        for i in range(len(test_case)):
            req, pre_result, exception = test_case[i]

            test_req_data = {
                "author": "admin",
                "system-root": self.system_config.get_system_root(),
                "target-root": req,
            }
            if not pre_result:
                # 실패
                self.assertRaises(exception, lambda: test_make_directory(test_req_data))
                # 디렉토리가 존재해서는 안된다.
                self.assertEqual(os.path.isdir(f"{self.cur_root}{self.token}{req}"), False)
            else:
                # 성공
                test_make_directory(test_req_data)
                # 디렉토리가 존재해야 한다.
                self.assertEqual(os.path.isdir(f"{self.cur_root}{self.token}{req}"), True)

    def test_remove_new_directory(self):
        # 디렉토리 제거 테스트

        directory_list = ["aaa", "bbb", f"aaa{self.token}ccc"]
        test_case = [
            (f"sdflsa", False, MicrocloudchipDirectoryNotFoundError),
            (f"aaa{self.token}zzz", False, MicrocloudchipDirectoryNotFoundError),
            (f"bbb", True, None),
            (f"aaa{self.token}ccc", True, None),
            (f"aaa", True, None)
        ]

        # 테스트를 위한 디렉토리 생성
        for dir in directory_list:
            req_data = {
                "author": "admin",
                "system-root": self.system_config.get_system_root(),
                "target-root": dir
            }
            test_make_directory(req_data)
            self.assertEqual(os.path.isdir(f"{self.cur_root}{self.token}{dir}"), True)

        # 삭제
        for i in range(len(test_case)):
            dir, pre_result, exception = test_case[i]
            req_data = {
                "author": "admin",
                "system-root": self.system_config.get_system_root(),
                "target-root": dir
            }
            if not pre_result:
                # 실패일 경우
                self.assertRaises(exception, lambda: test_remove_directory(req_data))
                # 실패이므로 디렉토리가 존재해야 한다.
                self.assertEqual(os.path.isdir(f"{self.cur_root}{self.token}{dir}"), True)
            else:
                test_remove_directory(req_data)
                # 성공이므로 삭제가 되어야 한다.
                self.assertEqual(os.path.isdir(f"{self.cur_root}{self.token}{dir}"), False)

    def test_upload_file(self):
        # 파일 가상 업로드 하기
        pass

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
