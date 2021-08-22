from django.http import JsonResponse

from module.MicrocloudchipException.exceptions import *
from module.session_control import session_control
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
    except KeyError:
        # request에 해당 데이터가 존재하지 않는 경우
        e = MicrocloudchipAuthAccessError("Access Failed")
        return JsonResponse({
            "code": e.errorCode
        })
    except MicrocloudchipLoginFailedError as e:
        return JsonResponse({
            "code": e.errorCode
        })

    # 통과
    # 세션 저장
    session_control.login_session_event(request, user_data['static-id'])
    return JsonResponse({
        "code": 0x00,
        "data": user_data
    })


@api_view(['GET'])
def view_user_logout(request: Request) -> JsonResponse:
    print(session_control.is_logined_event(request))

    session_control.logout_session_event(request)
    return JsonResponse({
        "code": 0x00
    })
