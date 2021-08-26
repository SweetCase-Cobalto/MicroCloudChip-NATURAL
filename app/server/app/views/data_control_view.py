from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse, QueryDict
from rest_framework.request import Request
from rest_framework.views import APIView
from module.MicrocloudchipException.exceptions import *
from module.session_control.session_control import is_logined_event, get_static_id_in_session
from . import *


class DataControlView(APIView):
    """
        data_type: file / dir(Directory)
        static_id: 유저 아이디
        root: 파일 및 디렉토리 범위
    """

    @staticmethod
    def check_is_logined(request: Request):
        # 로그인 되어있는 지 체크
        if not is_logined_event(request):
            raise MicrocloudchipLoginConnectionExpireError("Login Expired")

    def post(self, request: Request, data_type: str, static_id: str, root: str):

        # Session 상태 확인
        try:
            DataControlView.check_is_logined(request)
        except MicrocloudchipLoginConnectionExpireError as e:
            return JsonResponse({'code': e.errorCode})

        # 요청 아이디 획득
        req_static_id: str = get_static_id_in_session(request)

        # 파일 데이터 획득
        if data_type == 'file':

            data: QueryDict = request.data  # 파일 데이터가 포함되어 들어온다.
            try:
                uploaded_file: InMemoryUploadedFile = data.get('file')
            except KeyError:
                err = MicrocloudchipSystemAbnormalAccessError("Reqeust Data invalid Error")
                return JsonResponse({'code': err.errorCode})

            # Manager 에 생성 요청을 위한 Input Data
            req = {
                'static-id': static_id,
                'target-root': root,
                'raw-data': uploaded_file.read()
            }
            try:
                # 생성
                STORAGE_MANAGER.upload_file(
                    req_static_id,
                    req, USER_MANAGER
                )
            except MicrocloudchipException as e:
                return JsonResponse({"code": e.errorCode})

            # 파일 및 디렉토리 업로드
        elif data_type == 'dir':
            req = {
                'static-id': static_id,
                'target-root': root
            }
            try:
                STORAGE_MANAGER.generate_directory(req_static_id, req)
            except MicrocloudchipException as e:
                return JsonResponse({"code": e.errorCode})

        else:
            # 접근 에러
            err = MicrocloudchipSystemAbnormalAccessError("Access Error")
            return JsonResponse({'code': err.errorCode})
        return JsonResponse({"code": 0})

    def get(self, request: Request, data_type: str, static_id: str, root: str):
        # 데이터[정보] 갖고오기
        return JsonResponse({"code": 0})

    def patch(self, request: Request, data_type: str, static_id: str, root: str):
        # 파일 및 디렉토리 수정

        # Session 상태 확인
        try:
            DataControlView.check_is_logined(request)
        except MicrocloudchipLoginConnectionExpireError as e:
            return JsonResponse({'code': e.errorCode})

        # 요청 아이디 획득
        req_static_id: str = get_static_id_in_session(request)

        # 변경 데이터
        data: QueryDict = request.data

        if data_type == 'file':

            # 변경 대상 파일 이름을 찾는다.
            try:
                file_name: str = data.get('filename')
            except KeyError:
                err = MicrocloudchipSystemAbnormalAccessError("Reqeust Data invalid Error")
                return JsonResponse({'code': err.errorCode})

            # 확장자를 추출한다.
            splited_target_file_name = root.split('/')[-1].split('.')

            # 확장자가 존재하는 경우 file_name에 기존 확장자를 추가한다.
            if len(splited_target_file_name) >= 2:
                file_name += f".{splited_target_file_name[-1]}"

            # 수정 요청 데이터 작성
            req = {
                'static-id': static_id,
                'target-root': root,
                'change': {
                    'name': file_name
                }
            }
            try:
                STORAGE_MANAGER.update_file(req_static_id, req)
            except MicrocloudchipException as e:
                return JsonResponse({'code': e.errorCode})

        elif data_type == 'dir':

            # 디렉토리일 경우
            try:
                dir_name: str = data.get('dir_name')
            except KeyError:
                err = MicrocloudchipSystemAbnormalAccessError("Reqeust Data invalid Error")
                return JsonResponse({'code': err.errorCode})

            # 수정 요청 데이터 작성
            req = {
                'static-id': static_id,
                'target-root': root,
                'change': {
                    'name': dir_name
                }
            }
            try:
                # 디렉토리 정보 수정
                STORAGE_MANAGER.update_directory(req_static_id, req)
            except MicrocloudchipException as e:
                return JsonResponse({'code': e.errorCode})
        else:
            err = MicrocloudchipSystemAbnormalAccessError("Access Error")
            return JsonResponse({'code': err.errorCode})

        return JsonResponse({"code": 0})

    def delete(self, request: Request, data_type: str, static_id: str, root: str):
        # 파일 및 디렉토리 삭제
        # Session 상태 확인
        try:
            DataControlView.check_is_logined(request)
        except MicrocloudchipLoginConnectionExpireError as e:
            return JsonResponse({'code': e.errorCode})

        req_static_id: str = get_static_id_in_session(request)

        req = {
            'static-id': static_id,
            'target-root': root
        }

        try:
            if data_type == 'file':
                STORAGE_MANAGER.delete_file(req_static_id, req)
            elif data_type == 'dir':
                STORAGE_MANAGER.delete_directory(req_static_id, req)
            else:
                err = MicrocloudchipSystemAbnormalAccessError("Access Error")
                return JsonResponse({'code': err.errorCode})
        except MicrocloudchipException as e:
            return JsonResponse({'code': e.errorCode})
        
        # 성공 시
        return JsonResponse({"code": 0})
