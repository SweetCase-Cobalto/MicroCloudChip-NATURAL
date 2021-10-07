from django.http import JsonResponse

from module.MicrocloudchipException.base_exception import MicrocloudchipException
from module.MicrocloudchipException.exceptions import MicrocloudchipLoginConnectionExpireError, \
    MicrocloudchipSystemAbnormalAccessError, MicrocloudchipUserDoesNotExistError, MicrocloudchipAuthAccessError
from . import *
from rest_framework.request import Request


# Atom Function
def __check_token(request: Request) -> str:
    # 실제 Token Checker Routine
    try:
        token: str = request.headers.get('Set-Cookie')
        req_static_id, updated_token = TOKEN_MANAGER.is_logined(token)
        if not req_static_id:
            e = MicrocloudchipLoginConnectionExpireError("Login expired")
            raise e
    except MicrocloudchipException as e:
        raise e
    else:
        return req_static_id, updated_token


def __check_is_admin(static_id: str) -> bool:
    # 어드민 권한 여부 체크
    user_info: dict = USER_MANAGER.get_user_by_static_id(static_id, static_id)

    # 데이터 찾기 실패
    if not user_info:
        raise MicrocloudchipUserDoesNotExistError("User does not exist")
    return user_info['is-admin']


# Decorator Functions
def check_token(func):
    # Token Checker
    def wrapper(request, *args, **kwargs):

        try:
            # Tokne checking
            req_static_id, updated_token  = __check_token(request)
        except MicrocloudchipException as e:
            return JsonResponse({'code': e.errorCode})
        else:
            # static_id 데이터를 view의 파라미터에 강제 추가한다
            # 헤더 재정의
            kwargs['req_static_id'] = req_static_id
            kwargs['updated_token'] = updated_token
            return func(request, *args, **kwargs)

    return wrapper


def check_token_in_class_view(func):
    def wrapper(view_instance, *args, **kwargs):
        request: Request = args[0]
        try:
            req_static_id, updated_token = __check_token(request)
        except MicrocloudchipException as e:
            return JsonResponse({'code': e.errorCode})
        else:
            kwargs['req_static_id'] = req_static_id
            kwargs['updated_token'] = updated_token
            return func(view_instance, *args, **kwargs)

    return wrapper


def check_is_admin(func):
    def wrapper(request: Request, *args, **kwargs):
        try:
            req_static_id = kwargs['req_static_id']
        except KeyError:
            e = MicrocloudchipAuthAccessError("request static id does not exist")
            print(e)
            return JsonResponse({'code': e.errorCode})

        if not __check_is_admin(req_static_id):
            # Admin 아님
            e = MicrocloudchipAuthAccessError("You are not admin")
            return JsonResponse({'code': e.errorCode})
        else:
            return func(request, *args, **kwargs)

    return wrapper


def check_is_admin_in_class_view(func):
    def wrapper(view_instance, *args, **kwargs):
        request: Request = args[0]
        try:
            req_static_id = kwargs['req_static_id']
        except KeyError:
            e = MicrocloudchipAuthAccessError("request static id does not exist")
            print(e)
            return JsonResponse({'code': e.errorCode})

        if not __check_is_admin(req_static_id):
            # Admin 아님
            e = MicrocloudchipAuthAccessError("You are not admin")
            return JsonResponse({'code': e.errorCode})
        else:
            return func(view_instance, *args, **kwargs)

    return wrapper
