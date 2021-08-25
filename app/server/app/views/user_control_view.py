from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse, QueryDict
from rest_framework.request import Request
from rest_framework.views import APIView

from module.MicrocloudchipException.exceptions import *
from module.label.file_type import FileVolumeType
from module.label.user_volume_type import UserVolumeType
from module.session_control.session_control import is_logined_event

from . import *


class UserControlView(APIView):
    UPDATE_USER_ATTRIBUTES: list[str] = ['name', 'password', 'volume-type']

    # 변경 항목(선택)

    @staticmethod
    def check_is_logined(request: Request):
        if not is_logined_event(request):
            raise MicrocloudchipLoginConnectionExpireError("Login Expired")

    def patch(self, request: Request, static_id: str) -> JsonResponse:

        # Session 상태 확인
        UserControlView.check_is_logined(request)

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

    def get(self, request: Request, static_id: str):
        # 유저 데이터 갖고오기

        # Session 상태 확인
        UserControlView.check_is_logined(request)

        # 데이터 갖고오기
        user_info: dict = USER_MANAGER.get_user_by_static_id(static_id)

        # 못찾음
        if not user_info:
            e = MicrocloudchipUserDoesNotExistError("User is not exist")
            return JsonResponse({'code': e.errorCode})

        # 제한 용량 Json 형식에 맞추어 자료형 변경하기
        user_volume_type: UserVolumeType = user_info['volume-type']

        t = user_volume_type.to_tuple()

        user_volume_type: FileVolumeType = t[0]
        user_volume_type_str: str = user_volume_type.name
        # 왼쪽: 유저 사용 가능 용량의 타입(KB, MB, GB ..)
        user_volume_type_val: int = t[1]
        # 우측: 사용 가능 값(1, 1000 ...)

        # 두개 다 합치면 1KB, 1GB 등이 된다.

        # user_info 수정하기
        del user_info['volume-type']
        user_info['volume-type']: dict = {
            "type": user_volume_type_str,
            "value": user_volume_type_val
        }

        # 사용량 갖고오기
        used_size_tuple: tuple = USER_MANAGER.get_used_size(static_id)

        # 자료형 표기를 위해 일부너 여러줄 작성
        volume_type: FileVolumeType = used_size_tuple[0]
        volume_val: float = used_size_tuple[1]
        volume_type_to_str = volume_type.name

        # 결과 데이터 갖고오기
        res: dict = {
            "code": 0,
            "user-info": user_info,
            "used-volume": {
                'type': volume_type_to_str,
                'value': volume_val
            }
        }

        return JsonResponse(res)
