from django.test import TestCase

from module.data_builder.user_builder import UserBuilder
from module.specification.System_config import SystemConfig
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

    # User 저장소
    test_user_root: str = f"{system_config.get_system_root()}\\storage\\" if sys.platform == "win32" \
        else f"{system_config.get_system_root()}/storage/"
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
        # 해당 User Directory 가 정상적으로 저장되었는 지 확인
        pass

    def test_remove_new_directory(self):
        # 디렉토리 삭제
        pass

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