from django.http import JsonResponse

import app.models as model
from module.MicrocloudchipException.exceptions import MicrocloudchipSystemAbnormalAccessError, \
    MicrocloudchipLoginFailedError
from . import USER_MANAGER, STORAGE_MANAGER

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
        e = MicrocloudchipSystemAbnormalAccessError("Access Failed")
        return JsonResponse({
            "code": e.errorCode
        })
    except MicrocloudchipLoginFailedError as e:
        return JsonResponse({
            "code": e.errorCode
        })

    return JsonResponse({
        "code": 0x00,
        "data": user_data
    })
