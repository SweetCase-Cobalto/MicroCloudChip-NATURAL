from django.test import TestCase

from module.data_builder.user_builder import UserBuilder
from app.models import User


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

    def setUp(self) -> None:
        user_builder = UserBuilder()
        user_builder.set_name("admin") \
            .set_email("seokbong60@gmail.com") \
            .set_password("1234567890") \
            .set_is_admin(True) \
            .set_volume_type("TEST") \
            .set_static_id() \
            .build().save()

    def test_make_new_directory(self):
        # 디렉토리 생성 테스트
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

