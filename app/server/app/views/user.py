from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse

from module.MicrocloudchipException.exceptions import *
from . import *

from rest_framework.decorators import api_view
from rest_framework.request import Request


@api_view(['POST'])
def view_user_login(request: Request) -> JsonResponse:
    # Form 을 이용해 받지 않기 때문에 Form.py 사용 안함
    try:
        email: str = request.data['email']
        pswd: str = request.data['pswd']
        user_data: dict = USER_MANAGER.login(email, pswd)

        static_id: str = user_data['static-id']

        # 토큰 저장
        user_data['token'] = TOKEN_MANAGER.login(static_id)
    except KeyError:
        # request에 해당 데이터가 존재하지 않는 경우
        e = MicrocloudchipSystemAbnormalAccessError("Access Failed")
        return JsonResponse({
            "code": e.errorCode
        })
    except MicrocloudchipException as e:
        return JsonResponse({
            "code": e.errorCode
        })
    
    # 결과값 리턴
    return JsonResponse({
        "code": 0x00,
        "data": user_data
    })


@api_view(['GET'])
def view_user_logout(request: Request) -> JsonResponse:
    # 쿠키에 있는 토큰 갖고오기
    try:
        token: str = request.COOKIES['web-token']
    except Exception:
        raise MicrocloudchipSystemAbnormalAccessError("Token is nothing - error")
    TOKEN_MANAGER.logout(token)
    return JsonResponse({
        "code": 0x00
    })


@api_view(['POST'])
def view_add_user(request: Request) -> JsonResponse:

    # 로그인 확인
    try:
        token: str = request.COOKIES['web-token']
        req_static_id: str = TOKEN_MANAGER.is_logined(token)
        if not req_static_id:
            e = MicrocloudchipLoginConnectionExpireError("Login expired")
            return JsonResponse({'code': e.errorCode})
    except KeyError:
        e = MicrocloudchipSystemAbnormalAccessError("Token is nothing - error")
        return JsonResponse({'code': e.errorCode})

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
    err: MicrocloudchipException = MicrocloudchipSucceed()
    try:
        # 추가
        USER_MANAGER.add_user(req_static_id, user_req)
    except MicrocloudchipException as e:
        err = e
    finally:
        return JsonResponse({"code": err.errorCode})
