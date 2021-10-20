from django.test import TestCase
import json

from app.tests.test_modules.loader import test_flow, TestCaseFlow, TestCaseFlowRunner
from module.MicrocloudchipException.base_exception import MicrocloudchipException
from module.data.user_data import UserData

from app.tests.test_modules.testing_user_module import *


class UserUnittest(TestCase):
    """
        유저 생성만 테스트 하고
        수정 및 삭제는 Manager 단계에서 진행한다.
    """

    CONFIG_FILE_ROOT: str = ["server", "config.json"]
    TEST_CASE_FILE_ROOT: str = ["app", "tests", "test-input-data", "user", "test-case.json"]
    EXAMPLE_IMAGE_ROOT: str = ["app", "tests", "test-input-data", "user"]

    static_id_list: list[str] = []

    # 실제 등록된 config 파일에서 작동
    # 따라서 테스트 하기 전에 migration 을 반드시 해야 한다.
    config: SystemConfig = SystemConfig(os.path.join(*CONFIG_FILE_ROOT))

    @classmethod
    def setUpClass(cls):
        # 테스트 파일이 정상적으로 존재하는 지 확인
        super(UserUnittest, cls).setUpClass()

        test_case_file_root_str = os.path.join(*UserUnittest.TEST_CASE_FILE_ROOT)
        if not os.path.isfile(test_case_file_root_str):
            raise NotADirectoryError(f"{test_case_file_root_str} is not exist")

    def test_add_user(self):
        """ TestCase(user/test-case.json)에 대한 설명
        1. 데이터가 빠져있는 것에 대한 측정(전부다 parsing 에 실패해야 한다)
        2. 데이터 유효성 측정(예도 전부다 false)
        3. 유효성에 통과되는 데이터
            그러나 중복 검사를 통해 일부는 false 처리가 된다
        """

        # 정상적인 request 만 골라서 DB에 저장할 수 있는지 테스트한다.
        # True 로 판정될 경우 실제로 DB에 저장한다
        # 이미지 업로드 기능은 API 단계에서 테스트한다 여기서는 그냥 샘플페이지를 사용

        # 테스트 케이스 갖고오기
        test_case_file_root_str = os.path.join(*UserUnittest.TEST_CASE_FILE_ROOT)
        with open(test_case_file_root_str) as _f:
            test_cases = json.load(_f)["test-case"]

        for idx, test_case in enumerate(test_cases):
            user_builder = UserBuilder()

            req = test_case['request']
            if not test_case["is-passed"]:
                # 실패 케이스일 경우
                self.assertRaises(MicrocloudchipException,
                                  lambda: test_add_user(user_builder, req, self.config.system_root))
            else:
                # Success
                test_add_user(user_builder, req, self.config.system_root)

                # 다음 테스트에 사용할 static_id 추가
                self.static_id_list.append(user_builder.static_id)

        # 디렉토리 초기화
        test_reset_because_of_failed_upload_failed(self.static_id_list, self.config.get_system_root())

    @test_flow("app/tests/test-input-data/user/test_modify_user.json")
    def test_modify_user(self, test_flow: TestCaseFlow):

        def __cmd_add_user(
                name: str,
                pswd: str,
                email: str,
                volume_type: str,
                is_admin: bool
        ):
            UserBuilder().set_name(name) \
                .set_email(email) \
                .set_password(pswd) \
                .set_is_admin(is_admin) \
                .set_volume_type(volume_type) \
                .set_static_id() \
                .set_system_root(self.config.system_root) \
                .save()

        def __cmd_modify_username(target_email: str, n_name: str, is_succeed: bool, exception_str: str):
            try:
                d: UserData = UserData(email=target_email, system_root=self.config.system_root)()
                d.update(new_name=n_name)

            except MicrocloudchipException as e:
                # Failed
                self.assertFalse(is_succeed)
                self.assertEqual(type(e).__name__, exception_str)
            except Exception as e:
                print(f"[External Error]: {type(e)}:{e}")
                print(f"[Req]: {target_email}:{n_name}:{is_succeed}:{exception_str}")
            else:
                # Succeed
                self.assertTrue(is_succeed, msg=n_name)

        def __cmd_modify_password(target_email: str, new_password: str, is_succeed: bool, exception_str: str):
            try:
                d: UserData = UserData(email=target_email, system_root=self.config.system_root)()
                d.update(new_password=new_password)
            except MicrocloudchipException as e:
                # Failed
                self.assertFalse(is_succeed)
                self.assertEqual(type(e).__name__, exception_str)
            else:
                # Succeed
                self.assertTrue(is_succeed)

        def __cmd_modify_volumetype(target_email: str, volume_type: str, is_succeed: bool, exception_str: str):
            try:
                d: UserData = UserData(email=target_email, system_root=self.config.system_root)()
                d.update(new_volume_type=volume_type)
            except MicrocloudchipException as e:
                # Failed
                self.assertFalse(is_succeed)
                self.assertEqual(type(e).__name__, exception_str)
            else:
                # Succeed
                self.assertTrue(is_succeed)

        def __cmd_modify_image(target_email: str, img_name: str, is_succeed: bool, exception_str: str):

            img_root: str = os.path.join(*(self.EXAMPLE_IMAGE_ROOT + [img_name]))
            with open(img_root, 'rb') as _f:
                img_raw_data = _f.read()

            try:
                d: UserData = UserData(email=target_email, system_root=self.config.system_root)()
                d.update(will_change_image=True, img_extension=img_root.split('.')[-1], img_raw_data=img_raw_data)
            except MicrocloudchipException as e:
                self.assertFalse(is_succeed)
                self.assertEqual(type(e).__name__, exception_str)
            else:
                self.assertTrue(is_succeed)

        # Run Test Code
        TestCaseFlowRunner(test_flow).set_process('add-user', __cmd_add_user) \
            .set_process("modify-username", __cmd_modify_username) \
            .set_process("modify-password", __cmd_modify_password) \
            .set_process("modify-volumetype", __cmd_modify_volumetype) \
            .set_process("modify-image", __cmd_modify_image) \
            .run()
