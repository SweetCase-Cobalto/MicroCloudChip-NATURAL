from django.http import JsonResponse

import app.models as model
from module.MicrocloudchipException.exceptions import MicrocloudchipSystemAbnormalAccessError

from rest_framework.decorators import api_view
from rest_framework.request import Request


@api_view(['POST'])
def view_user_login(request: Request) -> JsonResponse:
    # Form 을 이용해 받지 않기 때문에 Form.py 사용 안함
    try:
        email: str = request.data['email']
        pswd: str = request.data['pswd']
    except KeyError:
        e = MicrocloudchipSystemAbnormalAccessError("Access Failed")
        return JsonResponse({
            "code": e.errorCode
        })

    # 데이터 검색
    return JsonResponse({
        "hello": "world"
    })
