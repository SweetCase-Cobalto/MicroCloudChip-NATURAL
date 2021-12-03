from django.test import TestCase

from typing import List

from app.tests.test_modules.loader import test_flow, TestCaseFlow, TestCaseFlowRunner


class TestNativeSearchTools(TestCase):
    """
        검색 관련 툴 테스트 클래스
        1. 파일/디렉토리 이름 문자열 매칭
    """
    TEST_FILE_ROOT: str = "app/tests/test-input-data/search"

    def __search_storage_name(self, regex: str, input_datas: List[str], output_datas: List[str]):
        # Set Search System
        from module.tools.search import StorageNameSearcher

        searched_list = []
        # 검색된 문자열

        search_system: StorageNameSearcher = StorageNameSearcher(regex)

        for data in input_datas:
            #  문자열 매칭 시작
            if search_system(data):
                searched_list.append(data)

        # 제대로 탐색이 되었는 지 확인
        searched_list.sort()
        output_datas.sort()

        self.assertListEqual(searched_list, output_datas, msg=f"ERROR REGEX: {regex}")

    @test_flow(f"{TEST_FILE_ROOT}/search_storage_name.json")
    def test_search_storage_name(self, test_flow: TestCaseFlow):
        TestCaseFlowRunner(test_flow) \
            .set_process("search-storage-names", self.__search_storage_name).run()
