---
description: 토큰 인증 Decorator 함수들
---

# Token Decorators

매번 server api 접근을 할 때마다 클라이언트로부터 보내오는 token 인증을 실시합니다. 하지만  [Code Test](https://seokbong60.gitbook.io/microcloudchip-natural/v/v0.0.x/wiki-for-developers/tdd-test-driven-development/testflow-module) 때첨 복붙 할 수는 없기 때문에 Decorator 함수를 사용합니다.

## \__check_token

데코레이터 함수가 아닌 클라이언트로부터 받은 Request에서 token을 뽑아내 인증 메소드를 통해 검토하는 raw method입니다

```python
# Atom Function
def __check_token(request: Request) -> str:
    # 실제 Token Checker Routine
    try:
        token: str = request.headers.get('Set-Cookie')
        req_static_id: str = TOKEN_MANAGER.is_logined(token)
        if not req_static_id:
            e = MicrocloudchipLoginConnectionExpireError("Login expired")
            raise e
    except KeyError:
        e = MicrocloudchipSystemAbnormalAccessError("Token is nothing - error")
        raise e
    else:
        return req_static_id
```

* line 5: 클라이언트로 받은 request 객체에서 cookie를 통해 token를 뽑아 옵니다
* line 6: token manager를 통해 token 인증을 거칩니다. 올바른 token이 아니면 NoneType을 반환합니다. 
* line 7: 올바른 token이 아닐 경우 Error를 호출합니다.
* line 10: cookie 안에 token이 아예 없어서 KeyError를 호출하는 경우도 있습니다.
* line 14: 제대로 된 token이 맞으면 token에 해당되는 사용자 id를 반환합니다.

## check_token

check token 메소드를 views에서 사용할 수 있게 decorator화 합니다.

### Code

```python
def check_token(func):
    # Token Checker
    def wrapper(request, *args, **kwargs):
        try:
            # Tokne checking
            req_static_id: str = __check_token(request)
        except MicrocloudchipException as e:
            return JsonResponse({'code': e.errorCode})
        else:
            # static_id 데이터를 view의 파라미터에 강제 추가한다
            # 헤더 재정의
            kwargs['req_static_id'] = req_static_id
            return func(request, *args, **kwargs)
    return wrapper
```

* line 4 \~ 8: 위의 메소드를 활용해 token을 검토합니다.
* line 12: 검토가 완료되었으면 view의 파라메터가 dict형식으로 들어있는 kwargs에 사용자 id를 추가합니다. 이렇게 되면 view 함수에서는 req static id라는 파라미터 변수가 추가됩니다.
* line 13: view 메소드를 실행합니다.

### [Example](https://github.com/SweetCase-Cobalto/microcloudchip-natural/blob/f75ff426b7fb0cca0edb7370e7beccd3593d4c08/app/server/app/views/user.py)

```python
@check_token
@api_view(['POST'])
def view_add_user(request: Request, req_static_id: str) -> JsonResponse:
    try:
        # 데이터 확인
        email: str = request.data['email']
        pswd: str = request.data['password']
        volume_type_str: str = request.data['volume-type']
        name: str = request.data['name']
    except KeyError:
        _e = MicrocloudchipSystemAbnormalAccessError("Access Failed")
        return JsonResponse({
            'code': _e.errorCode
        })
        ... 생략 ...
```

* line 1: 맨 위에 check_token decorator가 실행됩니다.
* line 3: 그에 따라 해당 메소드의 맨 마지막 부분에 req static id가 추가되었습니다.

## check_token_in_class_view

아까 위의 메소드는 DJango의 APIView 에서는 사용할 수가 없습니다. 그 이유는,  Class 멤버 메소드가 아닌 일반 메소드일 경우, Request 객체가 맨 앞에 오지만, APIView는 객체 데이터인 self가 먼저 들어옵니다. 따라서 APIView 전용 Decorator 메소드를 따로 구현했습니다.

### Code

```python
def check_token_in_class_view(func):
    def wrapper(view_instance, *args, **kwargs):
        request: Request = args[0]
        try:
            req_static_id: str = __check_token(request)
        except MicrocloudchipException as e:
            return JsonResponse({'code': e.errorCode})
        else:
            kwargs['req_static_id'] = req_static_id
            return func(view_instance, *args, **kwargs)
    return wrapper
```

* line 2: APIView의 맨 첫번 째 파라미터는 self 이므로 Request가 아닌apiView 객체 자체인  view_instance가 들어갔습니다.
* line 4 \~ 7: token을 검토합니다
* line 9: token이 제대로 된 token일 경우 메소드의 parameter에 사용자 id를 추가합니다.
* line 10: 메소드를 실행합니다.

### [Example](https://github.com/SweetCase-Cobalto/microcloudchip-natural/blob/master/app/server/app/views/data_control_view.py)

```python
@check_token_in_class_view
def post(self, request: Request, data_type: str, static_id: str, root: str, req_static_id: str):
    # 파일을 업로드 하거나, 디렉토리를 생성합니다.

    try:
        root: str = DataControlView.get_real_root(root)
    except MicrocloudchipException as e:
        return JsonResponse({'code': e.errorCode})
    ... 생략 ...
```

* line 1: token 인증 decorator가 실행되었습니다
* line 2: parameter 맨 마지막 부분이 사용자 id가 파라미터로 추가되었습니다.

## check_is_admin

해당 어플리케이션에서는 유저 관리(추가/삭제) 같은 관리자만 수행할 수 있는 API가 있습니다. 관리자 관련 token을 거르는 decorator도 같이 구현되어 있습니다. 
