from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse, QueryDict
from rest_framework.request import Request
from rest_framework.views import APIView

from module.MicrocloudchipException.exceptions import *
from module.session_control.session_control import is_logined_event

from . import *


class UserControlView(APIView):
    UPDATE_USER_ATTRIBUTES: list[str] = ['name', 'password', 'volume-type']

    # 변경 항목(선택)

    def patch(self, request: Request, static_id: str) -> JsonResponse:

        # Session 상태 확인
        if not is_logined_event(request):
            raise MicrocloudchipLoginConnectionExpireError("Login Expired")

        # 유저 정보의 일부를 업데이트한다.
        # 따라서 결과 값은 성공 여부가 된다.
        target_static_id: str = static_id  # 수정 대상 유저
        req_static_id: str = ""
        is_img_change: bool = False  # 유저 이미지 변경 여부

        req: dict = {}  # UserManager 에 유저 수정을 위한 Input Data

        data: QueryDict = request.data
        err: MicrocloudchipException = MicrocloudchipSucceed()
        # Key 값 찾기
        try:
            # 변경을 요청하는 아이디 갖고오기
            req_static_id = data.get('req-static-id')
            is_img_change = True if int(data.get('img-changeable')) else False
        except KeyError:
            err = MicrocloudchipAuthAccessError("Reqeust Data invalid Error")

        # UserManager에 변경을 요청하기 위한 데이터 생성
        req['static-id'] = target_static_id
        req['img-changeable'] = is_img_change
        req['img-raw-data'] = None
        req['img-extension'] = None

        for attr in UserControlView.UPDATE_USER_ATTRIBUTES:
            # 변경 항목 및 데이터 수집
            if attr in data:
                req[attr] = data.get(attr)

        # 이미지 추가 여부
        if req['img-changeable'] and 'img' in data:
            i: InMemoryUploadedFile = data.get('img')
            req['img-raw-data'] = i.read()
            req['img-extension'] = i.name.split('.')[-1]

        # 데이터 수정 요청
        try:
            USER_MANAGER.update_user(req_static_id, req)
        except MicrocloudchipException as e:
            err = e
        finally:
            return JsonResponse({"code": err.errorCode})
