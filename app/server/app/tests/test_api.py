from django.test import TestCase, Client
from django.http.response import JsonResponse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files import File
from django.test.client import encode_multipart

import app.models as model
from app.tests.test_modules.loader import test_flow, TestCaseFlow, TestCaseFlowRunner

from module.manager.storage_manager import StorageManager
from module.manager.token_manager import TokenManager
from module.manager.user_manager import UserManager
from module.specification.System_config import SystemConfig
from module.MicrocloudchipException.exceptions import *

SYSTEM_CONFIG: SystemConfig


class TestAPIUnittest(TestCase):
    client: Client
    admin_static_id: str

    USR_IMG_ROOT: str = 'app/tests/test-input-data/user/'
    FILES_ROOT: str = 'app/tests/test-input-data/example_files'

    BOUNDARY_VALUE: str = '123948572893'  # patch/delete 등에 사용하기위한 boudary 임의값

    @classmethod
    def setUpClass(cls) -> None:
        super(TestAPIUnittest, cls).setUpClass()

        # Admin
        SYSTEM_CONFIG = SystemConfig("server/config.json")
        UserManager(SYSTEM_CONFIG)
        StorageManager(SYSTEM_CONFIG)
        TokenManager(SYSTEM_CONFIG, 60)

    @staticmethod
    def make_uploaded_file(root: str) -> SimpleUploadedFile:
        f: File = File(open(root, 'rb'))
        u: SimpleUploadedFile = SimpleUploadedFile(
            f.name, f.read(), content_type='multipart/form-data'
        )
        return u

    @staticmethod
    def __get_user_id_for_test(user_name):
        return model.User.objects.get(name=user_name).static_id

    def check_exception_code(
            self,
            is_succeed: bool,
            error_code: int,
            expected_error_str: str,
            error_input: object = None
    ):
        expected_error_code: int = \
            0 if is_succeed else eval(expected_error_str)("").errorCode
        self.assertEqual(expected_error_code, error_code, msg=f"failed input: {error_input}")

    def setUp(self) -> None:
        self.client = Client()
        self.admin_static_id = model.User.objects.get(is_admin=True).static_id

    @test_flow("app/tests/test-input-data/test_api/test_login_logout.json")
    def test_login_logout(self, test_flow: TestCaseFlow):
        token_header: dict = {}

        def __cmd_login(
                email: str, password: str,
                is_succeed: bool, exception_str: str
        ):
            # Test Method: Login
            # Make Req
            req = {}
            if email:
                req['email'] = email
            if password:
                req['pswd'] = password
            # Send
            res: JsonResponse = self.client.post('/server/user/login', req)
            # Exception Code Check
            self.check_exception_code(is_succeed, res.json()["code"], exception_str, req)
            if is_succeed:
                # 성공시 token_header 갱신
                token_header["HTTP_Set-Cookie"] = res.json()["data"]['token']

        def __cmd_logout():
            # TODO Logout에 대한 특별한 예외는 없으며 차기 버전에 추가할 예정
            self.client.get("/server/user/logout", **token_header)

        TestCaseFlowRunner(test_flow).set_process("login", __cmd_login) \
            .set_process("logout", __cmd_logout).run()

    @test_flow("app/tests/test-input-data/test_api/test_user_add_and_delete.json")
    def test_user_add_and_delete(self, test_flow: TestCaseFlow):
        # 로그인이 안 된 상태에서 수행 불가

        # 만료되었다고 가정하는 임의의 쿠키
        token_header: dict = {"HTTP_Set-Cookie": "aldifjalsdkfjaldfkjaldskf"}

        def __cmd_login(
                email: str, password: str
        ):
            # Test Method: Login
            # Make Req
            req = {"email": email, "pswd": password}
            # Send
            res: JsonResponse = self.client.post('/server/user/login', req)
            token_header["HTTP_Set-Cookie"] = res.json()["data"]['token']

        def __cmd_add_user(
                name: str, email: str, password: str,
                volume_type_str: str, img: str,
                is_succeed: bool, exception_str: str
        ):

            req = dict()
            # if문 두줄짜리라 줄 없애려고 일부로 dict 씀
            """원래 구문
                if key:
                    req['key'] = value
            """
            if name:
                req['name'] = name
            if email:
                req['email'] = email
            if password:
                req['password'] = password
            if volume_type_str:
                req['volume-type'] = volume_type_str
            if img:
                req['img'] = TestAPIUnittest.make_uploaded_file(f"{self.FILES_ROOT}/{img}")
            res = self.client.post('/server/user', req, **token_header)

            # Exception Code Check
            self.check_exception_code(is_succeed, res.json()["code"], exception_str, req)

        def __cmd_modify_user(
                target: str,
                new_name: str, new_password: str,
                img_changeable: bool, img_name: str,
                is_succeed: bool, exception_str: str
        ):
            # Test Method: Modify User
            # static id 구하기
            target_id: str = self.__get_user_id_for_test(target)
            req = {}
            if new_name:
                req['name'] = new_name
            if new_password:
                req['password'] = new_password
            req['img-changeable'] = 1 if img_changeable else 0
            if img_name:
                req['img'] = self.make_uploaded_file(f"{self.FILES_ROOT}/{img_name}")

            res = self.client.patch(
                f"/server/user/{target_id}",
                data=encode_multipart(self.BOUNDARY_VALUE, req),
                content_type=f'multipart/form-data; boundary={self.BOUNDARY_VALUE}',
                **token_header
            )

            self.check_exception_code(is_succeed, res.json()["code"], exception_str, req)

        def __cmd_get_user_list(expected_users: list[str]):
            # Test Method: get user list
            # user가 제대로 검색 되었는 지 체크
            res = self.client.get("/server/user/list", **token_header)
            raw = res.json()
            self.assertFalse(raw['code'])
            searched_user_list = [user["username"] for user in raw["data"]]
            self.assertListEqual(sorted(expected_users), sorted(searched_user_list))

        def __cmd_get_user_info(
                target: str, is_raw_id: bool,
                is_succeed: bool, exception_str: str
        ):
            # Test Method: Get user Information
            target_id = target if is_raw_id else self.__get_user_id_for_test(target)
            res = self.client.get(f"/server/user/{target_id}", **token_header)
            self.check_exception_code(is_succeed, res.json()['code'], exception_str, target)

        def __cmd_remove_user(
                target: str, is_raw_id: bool,
                is_succeed: bool, exception_str: str
        ):
            # Test Method: remove user
            target_id = target if is_raw_id else self.__get_user_id_for_test(target)
            res = self.client.delete(f"/server/user/{target_id}", **token_header)
            self.check_exception_code(is_succeed, res.json()['code'], exception_str, target)

        # 테스트 실행
        TestCaseFlowRunner(test_flow) \
            .set_process('login', __cmd_login) \
            .set_process('add-user', __cmd_add_user) \
            .set_process('modify-user', __cmd_modify_user) \
            .set_process('get-user-info', __cmd_get_user_info) \
            .set_process('remove-user', __cmd_remove_user) \
            .set_process('get-user-list', __cmd_get_user_list) \
            .run()

    @test_flow("app/tests/test-input-data/test_api/test_add_modify_and_delete_data.json")
    def test_add_modify_and_delete_data(self, test_flow: TestCaseFlow):

        token_header: dict = {}

        def __cmd_login(
                email: str, password: str
        ):
            # Test Method: Login
            # Make Req
            req = {"email": email, "pswd": password}
            # Send
            res: JsonResponse = self.client.post('/server/user/login', req)
            token_header["HTTP_Set-Cookie"] = res.json()["data"]['token']

        def __cmd_upload_file(file_root: str, is_succeed: bool, exception_str: str):
            # Test Method: Upload file
            f: SimpleUploadedFile = \
                self.make_uploaded_file(f"{self.FILES_ROOT}/{file_root.split('/')[-1]}")
            # Run
            res = self.client.post(
                f'/server/storage/data/file/{self.admin_static_id}/root/{file_root}',
                data=encode_multipart(self.BOUNDARY_VALUE, {"file": f}),
                content_type=f'multipart/form-data; boundary={self.BOUNDARY_VALUE}',
                **token_header
            )
            # check result code
            self.check_exception_code(is_succeed, res.json()['code'], exception_str, file_root)

        def __cmd_generate_dir(dir_root: str, is_succeed: bool, exception_str: str):
            # Test Method: generate directory
            res = \
                self.client.post(
                    f"/server/storage/data/dir/{self.admin_static_id}/root/{dir_root}",
                    **token_header
                )
            self.check_exception_code(is_succeed, res.json()["code"], exception_str, dir_root)

        def __cmd_get_info(mode: str, root: str, is_succeed: bool, exception_str: str,
                           expected_files: list[str], expected_dirs: list[str]):
            # Test Method: get information of FILE or DIRECTORY
            uri = f"/server/storage/data/{mode}/{self.admin_static_id}/root"
            uri += f"/{root}" if root else ""
            res = self.client.get(uri, **token_header)
            self.check_exception_code(is_succeed, res.json()['code'], exception_str, [mode, root])

            # 디렉토리일 경우 하위 파일 / 디렉토리가 제대로 검색 되어있는 지 조사
            if mode == 'dir' and is_succeed:
                data = res.json()['data']['list']
                files, dirs = [f['name'] for f in data['file']], [d for d in data['dir']]
                self.assertListEqual(sorted(files), sorted(expected_files),
                                     msg=f"files not matched: {root}")
                self.assertListEqual(sorted(dirs), sorted(expected_dirs),
                                     msg=f"files not matched: {root}")

        def __cmd_modify_file(file_root: str, new_name: str, is_succeed: bool, exception_str: str):
            # Test Method: modify file information
            res = self.client.patch(
                f"/server/storage/data/file/{self.admin_static_id}/root/{file_root}",
                data=encode_multipart(self.BOUNDARY_VALUE, {"filename": {new_name}}),
                content_type=f'multipart/form-data; boundary={self.BOUNDARY_VALUE}',
                **token_header
            )
            self.check_exception_code(is_succeed, res.json()['code'],
                                      exception_str, [file_root, new_name])

        def __cmd_modify_dir(dir_root: str, new_name: str, is_succeed: bool, exception_str: str):
            # Test Method: modify directory imformation
            res = self.client.patch(
                f"/server/storage/data/dir/{self.admin_static_id}/root/{dir_root}",
                data=encode_multipart(self.BOUNDARY_VALUE, {"dir-name": {new_name}}),
                content_type=f'multipart/form-data; boundary={self.BOUNDARY_VALUE}',
                **token_header
            )
            self.check_exception_code(is_succeed, res.json()['code'], exception_str,
                                      [dir_root, new_name])

        def __cmd_remove(mode: str, root: str, is_succeed: bool, exception_str: str):
            # Test Method: remove file / directory
            res = self.client.delete(
                f"/server/storage/data/{mode}/{self.admin_static_id}/root/{root}", **token_header)
            self.check_exception_code(is_succeed, res.json()['code'], exception_str, [mode, root])

        # 테스트 코드 실행
        TestCaseFlowRunner(test_flow) \
            .set_process('login', __cmd_login) \
            .set_process('upload-file', __cmd_upload_file) \
            .set_process('generate-dir', __cmd_generate_dir) \
            .set_process('get-info', __cmd_get_info) \
            .set_process('modify-file-info', __cmd_modify_file) \
            .set_process('modify-dir-info', __cmd_modify_dir) \
            .set_process('remove', __cmd_remove) \
            .run()

    @test_flow("app/tests/test-input-data/test_api/test_storage_data_download.json")
    def test_storge_data_download(self, test_flow: TestCaseFlow):
        # 데이터 다운로드 관련 테스트
        CONTENT_TYPE_ZIP = "application/x-zip-compressed"

        token_header: dict = {}

        def __cmd_login(
                email: str, password: str
        ):
            # Test Method: Login
            # Make Req
            req = {"email": email, "pswd": password}
            # Send
            res: JsonResponse = self.client.post('/server/user/login', req)
            token_header["HTTP_Set-Cookie"] = res.json()["data"]['token']

        def __cmd_upload_file(file_root: str):
            # Test Method: Upload file
            f: SimpleUploadedFile = \
                self.make_uploaded_file(f"{self.FILES_ROOT}/{file_root.split('/')[-1]}")
            # Run
            self.client.post(
                f'/server/storage/data/file/{self.admin_static_id}/root/{file_root}',
                data=encode_multipart(self.BOUNDARY_VALUE, {"file": f}),
                content_type=f'multipart/form-data; boundary={self.BOUNDARY_VALUE}',
                **token_header
            )

        def __cmd_generate_dir(dir_root: str):
            # Test Method: generate directory
            self.client.post(
                f"/server/storage/data/dir/{self.admin_static_id}/root/{dir_root}",
                **token_header
            )

        def __cmd_download_single(mode: str, root: str, is_succeed: bool, exception_str: bool):
            # Test Method: download single file or directory
            uri = f"/server/storage/download/single/{mode}/{self.admin_static_id}/root"
            if mode == "file":
                uri += f"/{root}"
            elif mode == "dir":
                if root != "":
                    uri = f"/{root}"

            res = self.client.get(uri, **token_header)
            if res.headers['Content-Type'] == 'application/json':
                # 다운로드 실패
                self.check_exception_code(is_succeed, res.json()['code'], exception_str)

        def __cmd_download_multiple(params: dict[str], is_succeed: bool, exception_str: str):
            # Test Method: download multiple objects
            uri = f'/server/storage/download/multiple/{self.admin_static_id}/root'
            res = self.client.get(uri, data=params, **token_header)

            if res.headers['Content-Type'] == 'application/json':
                # 다운로드 실패
                self.check_exception_code(is_succeed, res.json()['code'], exception_str)
            if is_succeed:
                self.assertEqual(CONTENT_TYPE_ZIP, res.headers['Content-Type'])

        TestCaseFlowRunner(test_flow) \
            .set_process('login', __cmd_login) \
            .set_process('upload-file', __cmd_upload_file) \
            .set_process('generate-dir', __cmd_generate_dir) \
            .set_process('download-single', __cmd_download_single) \
            .set_process('download-multiple', __cmd_download_multiple) \
            .run()
