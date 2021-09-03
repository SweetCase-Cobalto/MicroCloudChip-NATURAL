from django.test import TestCase

from module.data_builder.user_builder import UserBuilder
from module.specification.System_config import SystemConfig
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
            ("aavvccs/vkdsfdsd", False, MicrocloudchipDirectoryNotFoundError),
            ("fs:fds:fd", False, MicrocloudchipFileAndDirectoryValidateError),
            ("fs*fds*fd", False, MicrocloudchipFileAndDirectoryValidateError),
            ("fs?fs?fs", False, MicrocloudchipFileAndDirectoryValidateError),
            ("fs>fs>fs", False, MicrocloudchipFileAndDirectoryValidateError),
            ("fs<fs<Fs", False, MicrocloudchipFileAndDirectoryValidateError),
            ('''fs"fs"fs''', False, MicrocloudchipFileAndDirectoryValidateError),
            ("fs|fs|fs", False, MicrocloudchipFileAndDirectoryValidateError),
            ("mydirectory", True, None),
            ("mydirectory", False, MicrocloudchipDirectoryAlreadyExistError),
            ("mydirectory/semidirectory", True, None)
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
            "success-after-make-directory": f"directory/{test_files[0]}",
            "failed": f"no/{test_files[1]}",
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
            self.assertEqual(test_upload_file_routine(req), True)

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
        self.assertEqual(test_upload_file_routine(file_req), True)
        # 중복 추가 불가능
        self.assertRaises(MicrocloudchipFileAlreadyExistError, lambda: test_upload_file_routine(file_req))

        # 실패
        __test_file = test_case['failed']
        __raw_data = self.get_raw_data_from_file(self.test_file_root + self.token + test_files[1])
        file_req['target-root'] = __test_file
        file_req['raw-data'] = __raw_data
        self.assertRaises(MicrocloudchipDirectoryNotFoundError, lambda: test_upload_file_routine(file_req))

    def test_get_information_of_file(self):

        # 데이터 정보 갖고오기

        # 이전 파일 저장
        example_files = os.listdir(self.test_file_root)
        author_static_id = model.User.objects.get(name="admin").static_id
        sys_root = self.system_config.get_system_root()

        # 파일 저장
        for ex in example_files:
            binary_data = self.get_raw_data_from_file(self.test_file_root + self.token + ex)
            req = {
                "static-id": author_static_id,
                "target-root": ex,
                "system-root": sys_root,
                "raw-data": binary_data
            }
            self.assertEqual(test_upload_file_routine(req), True)

        for ex in example_files:
            # 파일 정보 갖고오기
            req = {
                "static-id": author_static_id,
                "target-root": ex,
                "system-root": sys_root,
                "root-token": self.token
            }
            # Get File Information
            test_get_file_information(req)

        # 실패 케이스 추가
        req = {
            'static-id': author_static_id,
            "target-root": "man.txt",
            "system-root": self.system_config.get_system_root(),
            "root-token": self.token
        }
        # 파일 못찾음
        self.assertRaises(MicrocloudchipFileNotFoundError, lambda: test_get_file_information(req))

    def test_remove_file(self):
        # 파일 삭제

        example_files = os.listdir(self.test_file_root)
        file_name = example_files[0]
        author_static_id = model.User.objects.get(name="admin").static_id
        sys_root = self.system_config.get_system_root()

        binary_data = self.get_raw_data_from_file(self.test_file_root + self.token + file_name)
        req = {
            "static-id": author_static_id,
            "target-root": file_name,
            "system-root": sys_root,
            "raw-data": binary_data
        }
        self.assertEqual(test_upload_file_routine(req), True)

        del req['raw-data']
        req['root-token'] = self.token

        # 파일 데이터를 불러오고
        f_information = test_get_file_information(req)

        # 파일 삭제
        self.assertEqual(test_remove_file_routine(f_information), True)
        # 정상적으로 삭제되면 True 를 출력한다

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
