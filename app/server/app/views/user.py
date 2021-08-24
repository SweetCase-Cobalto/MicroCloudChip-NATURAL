from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse, QueryDict

from module.MicrocloudchipException.exceptions import *
from module.session_control import session_control
from . import *

from rest_framework.decorators import api_view
from rest_framework.request import Request

UPDATE_USER_ATTRIBUTES: list[str] = ['name', 'password', 'volume-type']


@api_view(['POST'])
def view_user_login(request: Request) -> JsonResponse:
    # Form 을 이용해 받지 않기 때문에 Form.py 사용 안함
    try:
        email: str = request.data['email']
        pswd: str = request.data['pswd']
        user_data: dict = USER_MANAGER.login(email, pswd)
    except KeyError:
        # request에 해당 데이터가 존재하지 않는 경우
        e = MicrocloudchipAuthAccessError("Access Failed")
        return JsonResponse({
            "code": e.errorCode
        })
    except MicrocloudchipException as e:
        return JsonResponse({
            "code": e.errorCode
        })

    # 통과
    # 세션 저장
    try:
        session_control.login_session_event(request, user_data['static-id'])
    except MicrocloudchipAuthAccessError as e:
        # 이미 로그인 했는데 또 로그인 한 경우
        # Microcloudchip AccessError 호출
        return JsonResponse({
            'code': e.errorCode
        })
    return JsonResponse({
        "code": 0x00,
        "data": user_data
    })


@api_view(['GET'])
def view_user_logout(request: Request) -> JsonResponse:
    session_control.logout_session_event(request)
    return JsonResponse({
        "code": 0x00
    })


@api_view(['POST'])
def view_add_user(request: Request) -> JsonResponse:
    if not session_control.is_logined_event(request):
        # 로그인 확인
        return JsonResponse({
            "code": MicrocloudchipLoginConnectionExpireError("").errorCode
        })

    try:
        # 데이터 확인
        req_static_id: str = request.data['req-static-id']
        email: str = request.data['email']
        pswd: str = request.data['password']
        volume_type_str: str = request.data['volume-type']
        name: str = request.data['name']
    except KeyError:
        _e = MicrocloudchipAuthAccessError("Access Failed")
        return JsonResponse({
            'code': _e.errorCode
        })

    # 이미지를 추가 안했다면 None으로 처리한다
    user_img: InMemoryUploadedFile = request.FILES['img'] if 'img' in request.FILES else None

    # 유저를 출력하기 위한 데이터 작성
    user_req: dict = {
        'name': name,
        'password': pswd,
        'email': email,
        'volume-type': volume_type_str,
        'img-raw-data': None if not user_img else user_img.read(),
        'img-extension': None if not user_img else user_img.name.split('.')[-1]
    }
    try:
        # 추가
        USER_MANAGER.add_user(req_static_id, user_req)
    except MicrocloudchipException as e:
        # 실패
        return JsonResponse({
            'code': e.errorCode
        })
    else:
        # 성공
        return JsonResponse({
            'code': 0x00
        })


@api_view(['PATCH', 'DELETE', 'GET'])
def view_user_control(request: Request, static_id: str) -> JsonResponse:
    if request.method == 'PATCH':
        print(request.POST)
        print("")

    return JsonResponse({'code': 0})
