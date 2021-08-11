from django.test import TestCase
import json

from module.specification.System_config import SystemConfig

from app.tests.test_modules.testing_user_module import *


class UserUnittest(TestCase):
    CONFIG_FILE_ROOT: str = ["server", "config.json"]
    TEST_CASE_FILE_ROOT: str = ["app", "tests", "test-input-data", "user", "test-case.json"]
    EXAMPLE_IMAGE_ROOT: str = ["app", "tests", "test-input-data", "user"]

    static_id_list: list[str] = []
    config: SystemConfig = SystemConfig(os.path.join(*CONFIG_FILE_ROOT))

    @classmethod
    def setUpClass(cls):
        super(UserUnittest, cls).setUpClass()

        test_case_file_root_str = os.path.join(*UserUnittest.TEST_CASE_FILE_ROOT)
        if not os.path.isfile(test_case_file_root_str):
            raise NotADirectoryError(f"{test_case_file_root_str} is not exist")

    @classmethod
    def tearDownClass(cls):
        # DB 데이터 죄다 삭제
        pass

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
                try:
                    # Req data validate
                    """set_info_to_user_builder:
                            user_builder 의 set 함수를 한꺼번에 사용하기 위한
                            함수
                    """
                    self.assertRaises(MicrocloudchipUserInformationValidateError,
                                      lambda: test_set_info_to_user_builder(user_builder, req))
                except AssertionError:
                    # Validator 를 통과했다면
                    # 업로드 과정에서 실패를 해야 한다.
                    try:
                        """test_upload_user_in_step_routinetest
                            User 등록 루틴 테스트 함수
                            실제로 User 등록 과정은 UserManager 가 담당하며
                            Manager 단계 Test 에서 다시 한번 테스트를 거친다.
                        """
                        test_set_info_to_user_builder(user_builder, req)
                        img_root: str = os.path.join(*(self.EXAMPLE_IMAGE_ROOT + ["example.png"]))
                        self.assertRaises(MicrocloudchipUserUploadFailedError,
                                          lambda: test_upload_user_in_step_routinetest(user_builder.build(),
                                                                                       self.config.get_system_root(),
                                                                                       img_root))
                    except AssertionError:
                        # 그래도 통과를 한 경우
                        print(f"problem number: {idx} is failed.")
                        # DB의 업로드한 User Data 와 저장한 image 파일을 지운다.
                        test_reset_because_of_failed_upload_failed(self.static_id_list + [user_builder.static_id],
                                                                   self.config.get_system_root())
                        raise
            else:
                # Success
                img_root: str = os.path.join(*(self.EXAMPLE_IMAGE_ROOT + ["example.png"]))
                test_set_info_to_user_builder(user_builder, req)
                test_upload_user_in_step_routinetest(user_builder.build(),
                                                     self.config.get_system_root(),
                                                     img_root)

                # 다음 테스트에 사용할 static_id 추가
                self.static_id_list.append(user_builder.static_id)

        test_reset_because_of_failed_upload_failed(self.static_id_list, self.config.get_system_root())
