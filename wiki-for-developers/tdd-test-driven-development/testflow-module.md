---
description: Test Solution Module
---

# TestFlow Module

## 개요

JSON에 있는 테스트 케이스를 불러와서 테스트를 하는 방식은 테스트를 변경/추가/삭제할 때 json 파일만 건들면 되기 때문에 편리합니다. 하지만 그렇다고 해서 json파일을 직접 읽와와서 진행하는 코드를 일일이 작성하기에는 적잖은 불편함이 따릅니다. 그래서 테스트 솔루션 Module인 TestCaseFlow와 TestCaseFlowRunner를 직접 구현해서 사용하고 있습니다. 특수한 경우가 아닌 이상 TestCaseFlow / TestCaseFlowRunner를 사용해서 테스트를 진행합니다

## Test Case Files

해당 프로젝트에서 사용하는 테스트 케이스 파일 내용은 대략 이와 같습니다

```
{
    "test-flow": [
        "type": [COMMAND]
        ...
    ]
}
```

* **test-flow:** test-flow는 테스트 식별자를 의미하며 TestCaseFlow는 Json 파일에서 "test-flow"의 value값을 이용해서 데이터를 가져옵니다
* **type:** 테스트 명령 내용 입력합니다. 예를 들어 "파일 추가", "파일 삭제" 같은 명령 이름 문자열 값을 작성합니다.

### 예제

```
{
  "test-flow": [
    {
      "type": "upload-file",
      "target": "admin", "request": "admin",
      "file-root": "example-text.txt"
    },
    ... 생략 ...
    {
      "type": "remove", "mode": "file",
      "target": "admin", "request": "client",
      "file-root": "example-text.txt",
      "is-succeed": false, "exception": "MicrocloudchipAuthAccessError"
    },
    ... 생략 ...
  ]
}
```

## TestCaseFlow

TestCaseFlow는 Test Json File을 불러와 순차적으로 큐에 테스트 케이스를 저장하는 클래스 입니다. TestCaseFlowRunner가 이 객체를 사용해서 테스트를 진행합니다.

### Class

```python
class TestCaseFlow:
    # 테스트 케이스를 저장하고 추출해서 사용하는 클래스
    test_flow: collections.deque
    commands: set[str]
```

* test_flow: Test Case를 저장하는 Queue 입니다.
* commands: 명령문을 저장합니다. Json File에서 "type"의 value값이 여기에 저장하게 됩니다.

### \__init\_\_

```python
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
```

test file의 경로를 입력받아서 Json 파일을 Load합니다. 테스트 케이스를 순회하며 테스트 케이스 안의 데이터 중에 value값만 뽑아와 case_arr에 저장합니다. 이 중  case arr의 첫 번 째 인덱스(0)는 명령문으로 commands에 저장하고 전체 데이터는 test flow에 저장합니다.

### Functions

```python
    def __call__(self) -> list:
        # 테스트 케이스 갖고오기
        return None if not self.test_flow else self.test_flow.pop()

    def is_empty(self):
        # 테스트 케이스를 죄다 사용했는 지 확인
        return len(self.test_flow) == 0

    def get_commands(self):
        return self.commands
```

* call: 테스트 케이스를 큐에서 불러옵니다. 비어있으면 NoneType을 반환합니다,
* is_empty: 테스트 큐가 비어있는 지 확인합니다
* get_commands: 명령문 집합을 불러옵니다.

## TestCaseFlowRunner

TestCaseFlow 객체를 사용하여 실제로 테스트를 진행하는 솔루션 객체입니다. 

### Class

```python
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
```

* test_flow: TestCaseFlow를 저장합니다.
* test_statements: 딕셔너리 형태로, key는 명령문, value는 실제 작동하는 함수를 저장하여 if문 없이 명령문에 따라 바로 테스트를 진행할 수 있게 합니다. set process 함수를 사용하여 관리합니다.

### Run Process

```python
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
```

* test_flow에서 케이스를 하나 씩 뽑아서 함수를 실행합니다.
* line 3 \~  line 5: Json으로 받은 테스트 명령문의 집합과 set_process이용해서 저장한 테스트 명령문의 집합이 일치하는 지 확인합니다. 그 이유는 Json으로 받은 테스트 명령문이 실제 테스트 코드로 등록되지 않으면 해당 명령문에 포함된 테스트 케이스를 무시하고 진행하기 때문에 원활한 테스트 진행이 되지 않습니다.
* line 8 \~ line 11: 매 턴 마다 test case를 하나 씩 뽑아서 진행합니다.
  * line 10: command는 테스트 명령문 , case는 테스트에 사용될 파라미터 입니다.
  * line 11: command와 case를 이용하여 테스트를 시행합니다.

## TestCaseFlow Decorator

Test Flow를 이용한 Test Case를 모으는 작업은 매 테스트 단위마다 실행해야 합니다. 그렇다고 매 테스트 단위마다 복사 붙여넣기 식으로 작성을 할 순 없고 또한 다른 객체의 상태를 변경하지 않는 순수 함수로 표현할 수 있기 때문에 Decorator Function으로 사용합니다.

### Decorator Function

```python
# TestCaseFlow Decorator
def test_flow(test_file_root: str):
    def __test_flow(func):
        def wrapper(*args, **kwargs):
            test_flow: TestCaseFlow = TestCaseFlow(test_file_root)
            kwargs['test_flow'] = test_flow
            func(*args, **kwargs)
        return wrapper
    return __test_flow
```

* line 5: test file root를 이용해 Json File 로부터 테스트 케이스를 모읍니다
* line 6: 실제 테스트 단위에 파라미터값으로 사용하기 위해 test_flow라는 parameter 변수로 생성합니다.
* line 7: 실제 함수를 실행합니다.

## [Example Code](https://github.com/SweetCase-Cobalto/microcloudchip-natural/blob/master/app/server/app/tests/test_api.py)

```python
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
    ... 생략 ...
    
    
    TestCaseFlowRunner(test_flow) \
            .set_process('login', __cmd_login) \
            .set_process('add-user', __cmd_add_user) \
            .set_process('modify-user', __cmd_modify_user) \
            .set_process('get-user-info', __cmd_get_user_info) \
            .set_process('remove-user', __cmd_remove_user) \
            .set_process('get-user-list', __cmd_get_user_list) \
            .run()
    
```

* line 1 \~ 2: test_flow decorator를 이용하여 테스트 케이스를 불러옵니다. 그 결과, line 2의 테스트 메소드 선언부에서 test flow가 추가되었습니다.
* line 8: 테스트를 시행하기 위한 테스트 메소드를 커스텀 합니다.
* line 21 \~ line 22: set process 메소드를 이용하여 테스트 명령문과 테스트 메소드를 등록합니다. 예를 들어 cmd login 함수는 'login' 명령문과 함 께 TestCaseFlowRunner에 등록되었습니다.
* line 22: 테스트를 시행합니다.
