import collections, json


class TestCaseFlow:
    test_flow: collections.deque

    def __init__(self, test_file_root: str):
        self.test_flow = collections.deque()

        with open(test_file_root, 'r', encoding='utf-8') as _f:
            raw = json.load(_f)['test-flow']
            for case in raw:
                case_arr = []
                for v in case.values():
                    case_arr.append(v)
                self.test_flow.appendleft(case_arr)

    def __call__(self) -> list:
        # 테스트 케이스 갖고오기
        return None if not self.test_flow else self.test_flow.pop()

    def is_empty(self):
        return len(self.test_flow) == 0


# TestCaseFlow Decorator
def test_flow(test_file_root: str):
    def __test_flow(func):
        def wrapper(*args, **kwargs):
            test_flow: TestCaseFlow = TestCaseFlow(test_file_root)
            kwargs['test_flow'] = test_flow
            func(*args, **kwargs)
        return wrapper
    return __test_flow
