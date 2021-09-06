from django.core.files.uploadedfile import InMemoryUploadedFile

from app.views.downloaders import *
from module.MicrocloudchipException.exceptions import *
from . import *

from rest_framework.decorators import api_view
from rest_framework.request import Request

from app.views.custom_decorators import check_token, check_is_admin


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
        token: str = request.headers.get('Set-Cookie')
    except Exception:
        raise MicrocloudchipSystemAbnormalAccessError("Token is nothing - error")
    TOKEN_MANAGER.logout(token)
    return JsonResponse({
        "code": 0x00
    })


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


@check_token
@check_is_admin
@api_view(['GET'])
def view_get_user_list(request: Request, req_static_id: str) -> JsonResponse:

    raw_user_data = USER_MANAGER.get_users()
    user_list_by_dict = []

    for _u in raw_user_data:
        user_list_by_dict.append({
            'username': _u.name,
            'user_static_id': _u.static_id,
            'userImgLink': None
        })

    return JsonResponse({'code': 0, 'data': user_list_by_dict})
