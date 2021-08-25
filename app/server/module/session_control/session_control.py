from enum import unique, Enum

from rest_framework.request import Request

from module.MicrocloudchipException.exceptions import *


@unique
class SessionKeys(Enum):
    STATIC_ID = 'static-id'


def is_logined_event(request: Request) -> bool:
    # 로그인 여부 확인
    if SessionKeys.STATIC_ID.value not in request.session:
        return False
    return True


def login_session_event(request: Request, static_id: str):

    # 이미 로그인을 한 경우
    if is_logined_event(request):
        raise MicrocloudchipSystemAbnormalAccessError("Aleady Logined")

    # 로그인 할 때 세션 저장
    request.session[SessionKeys.STATIC_ID.value] = static_id


def logout_session_event(request: Request):
    request.session.clear()
