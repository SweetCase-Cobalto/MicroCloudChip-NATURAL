from django.http import JsonResponse

from module.MicrocloudchipException.base_exception import MicrocloudchipException
from module.MicrocloudchipException.exceptions import MicrocloudchipLoginConnectionExpireError, \
    MicrocloudchipSystemAbnormalAccessError
from . import *
from rest_framework.request import Request


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
