from django.test import TestCase

"""
from module.specifications import Config
from module.exceptions import *
"""
import os


class AppBootingUnittest(TestCase):
    # Test File Roots
    TEST_DIR: str = "app/tests/test_input_data/app_booting"

    CONFIG_TEST_DIR: str = f"{TEST_DIR}/check_config_file_valid"
    CONFIG_INPUT_DIR: str = f"{CONFIG_TEST_DIR}/input"
    CONFIG_OUTPUT_EXPECT_RESULT: str = f"{CONFIG_TEST_DIR}/output.txt"

    @classmethod
    def setUpClass(cls):
        super(AppBootingUnittest, cls).setUpClass()
        # 테스트 파일 및 디렉토리가 제대로 있는 지 확인

        # 1. config check test
        if not os.path.isdir(AppBootingUnittest.CONFIG_INPUT_DIR):
            raise NotADirectoryError(f"{AppBootingUnittest.CONFIG_INPUT_DIR} is not exist")
        if not os.path.isfile(AppBootingUnittest.CONFIG_OUTPUT_EXPECT_RESULT):
            raise FileNotFoundError(f"{AppBootingUnittest.CONFIG_OUTPUT_EXPECT_RESULT} is not exist")

    def test_check_config_file_valid(self):
        import json

        # Server/config.json의 데이터가 올바르게 되어 있는 지 검사한다
        # 단 database는 이미 setting.py에서 검증하기 때문에 database를 제외한 나머지
        # 부분만 검사하면 된다

        def get_result_datas() -> dict:
            # TestCase 결과 데이터 불러오기
            results = {}
            with open(AppBootingUnittest.CONFIG_OUTPUT_EXPECT_RESULT, 'rt') as f:
                while True:
                    line = f.readline()[:-1]
                    if not line:
                        break
                    _problem_num, raw_result = line.split(':')
                    results[int(_problem_num)] = True if raw_result == "YES" else False
            return results

        expected_results = get_result_datas()

        # 돌아가면서 테스트를 수행한다.
        for problem_num, expected_result in expected_results.items():

            input_root = f"{self.CONFIG_INPUT_DIR}/example{problem_num}.json"
            # 파일이 존재하는 지 확인
            self.assertEqual(os.path.isfile(input_root), True)

            # 테스트 시작
            system_config = None
            if expected_result:
                # 파싱 성공이 정답인 경우
                system_config = SystemConfig(input_root)

                # System Root가 정상적으로 파싱이 되었는지 확인한다.
                expected_root = json.loads(open(input_root).readlines[:-1])['system']['storage-root']
                self.assertEqual(expected_root, system_config.get_system_root())
            else:
                # 실패를 해야 하는 경우
                def generate_system_config(input_file_root: str):
                    return SystemConfig(input_file_root)

                # 반드시 에러 발생
                self.assertRaises(MicroCloudChipSystemConfigFileParsingError, \
                                  generate_system_config, input_root)