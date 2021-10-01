import collections, json


class TestCaseFlow:
    # 테스트 케이스를 저장하고 추출해서 사용하는 클래스
    test_flow: collections.deque
    commands: set[str]

    def __init__(self, test_file_root: str):
        self.test_flow = collections.deque()
        self.commands = set()

        with open(test_file_root, 'r', encoding='utf-8') as _f:
            raw = json.load(_f)['test-flow']
            for case in raw:
                case_arr = []
                for v in case.values():
                    case_arr.append(v)
                if not case_arr[0] in self.commands:
                    # 명령문 저장(파일 업로드 etc)
                    self.commands.add(case_arr[0])
                self.test_flow.appendleft(case_arr)

    def __call__(self) -> list:
        # 테스트 케이스 갖고오기
        return None if not self.test_flow else self.test_flow.pop()

    def is_empty(self):
        # 테스트 케이스를 죄다 사용했는 지 확인
        return len(self.test_flow) == 0

    def get_commands(self):
        return self.commands


class TestCaseFlowRunner:
    # TestCase를 이용하 테스트 재생기
    test_flow: TestCaseFlow

    # Test Case 클래스를 상요하며
    # assert 함수를 사용할 때 참조
    test_statements: dict[str]

    def __init__(self, test_flow: TestCaseFlow):
        self.test_flow = test_flow
        self.test_statements = {}

    def set_process(self, cmd: str, func):
        # Builder Pattern 적용
        self.test_statements[cmd] = func
        return self

    def run(self):
        # checking commands
        if set(self.test_statements.keys()) != self.test_flow.get_commands():
            # 모든 command가 안들어가 있으면 테스트 진행 불가
            non_setted_cmds = self.test_flow.get_commands()
            raise TypeError(f"This Commands didn't setted: {list(non_setted_cmds)}")

        while not self.test_flow.is_empty():
            case = self.test_flow()
            command, case = case[0], case[1:]
            self.test_statements[command](*case)

    def is_empty(self):
        return self.test_flow.is_empty()


# TestCaseFlow Decorator
def test_flow(test_file_root: str):
    def __test_flow(func):
        def wrapper(*args, **kwargs):
            test_flow: TestCaseFlow = TestCaseFlow(test_file_root)
            kwargs['test_flow'] = test_flow
            func(*args, **kwargs)

        return wrapper

    return __test_flow
