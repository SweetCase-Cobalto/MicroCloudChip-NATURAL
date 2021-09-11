from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import QueryDict
from rest_framework.views import APIView
from module.MicrocloudchipException.exceptions import *
from module.data.storage_data import FileData, DirectoryData
from module.label.time import TIME_FORMAT
from app.views.custom_decorators import *
from . import *


class DataControlView(APIView):
    """ URL PARAMS
        data_type: file / dir(Directory)
        static_id: 유저 아이디
        root: 파일 및 디렉토리 범위
    """

    @staticmethod
    def get_real_root(root: str) -> str:
        """실제 루트 생성
            url 로부터 받은 root는 앞에 root/ 가 붙어있기 때문에
            root/ 를 제거하고 다시 정의한다

            EX) /root/abc/cdf --> abc/cdf
        """
        # 올바르지 않는 Root 확인

        """실제 루트 생성
            url 로부터 받은 root는 앞에 root/ 가 붙어있기 때문에
            root/ 를 제거하고 다시 정의한다
            EX) /root/abc/cdf --> abc/cdf
        """
        root_list = root.split('/')

        # URL 유효성 검토
        if len(root_list) == 1:
            if root_list[0] == 'root':
                return '/'.join(root_list[1:])
            else:
                raise MicrocloudchipFileAndDirectoryValidateError("Root Error")
        else:
            if '' in root_list:
                raise MicrocloudchipFileAndDirectoryValidateError("Root Error")
            else:
                return '/'.join(root_list[1:])

    @check_token_in_class_view
    def post(self, request: Request, data_type: str, static_id: str, root: str, req_static_id: str):
        # 파일을 업로드 하거나, 디렉토리를 생성합니다.

        try:
            root: str = DataControlView.get_real_root(root)
        except MicrocloudchipException as e:
            return JsonResponse({'code': e.errorCode})

        # 타입 축정
        if data_type == 'file':
            # 파일을 업로드 하는 경우

            data: QueryDict = request.data  # 파일 데이터가 포함되어 들어온다.
            try:
                # 클라이언트로 받은 업로드 요청된 파일
                uploaded_file: InMemoryUploadedFile = data.get('file')
            except KeyError:
                # 데이터가 없는 경우
                err = MicrocloudchipSystemAbnormalAccessError("Reqeust Data invalid Error")
                return JsonResponse({'code': err.errorCode})

            # Manager 에 생성 요청을 위한 Input Data
            req = {
                'static-id': static_id,
                'target-root': root,
                'raw-data': uploaded_file.read()
            }
            try:
                # 파일 생성
                STORAGE_MANAGER.upload_file(req_static_id, req, USER_MANAGER)
            except MicrocloudchipException as e:
                # 생성 실패
                return JsonResponse({"code": e.errorCode})

            # 파일 및 디렉토리 업로드
        elif data_type == 'dir':

            # 요청 Input Data
            req = {
                'static-id': static_id,
                'target-root': root
            }
            try:
                # 디렉토리 생성
                STORAGE_MANAGER.generate_directory(req_static_id, req)
            except MicrocloudchipException as e:
                return JsonResponse({"code": e.errorCode})

        else:
            # 접근 에러
            err = MicrocloudchipSystemAbnormalAccessError("Access Error")
            return JsonResponse({'code': err.errorCode})
        return JsonResponse({"code": 0})

    @check_token_in_class_view
    def get(self, request: Request, data_type: str, static_id: str, root: str, req_static_id: str) -> JsonResponse:
        # 데이터[정보] 갖고오기
        try:
            root: str = DataControlView.get_real_root(root)
        except MicrocloudchipFileAndDirectoryValidateError as e:
            return JsonResponse({'code': e.errorCode})

        # Input Data
        req = {
            'static-id': static_id,
            'target-root': root
        }
        if data_type == 'file':
            # 파일 정보 요청
            try:
                f: FileData = STORAGE_MANAGER.get_file_info(req_static_id, req)
            except MicrocloudchipException as e:
                return JsonResponse({'code': e.errorCode})
            return JsonResponse({
                'code': 0,
                'data': {
                    'create-date': f['create-date'].strftime(TIME_FORMAT),
                    'modify-date': f['modify-date'].strftime(TIME_FORMAT),
                    'file-name': f['file-name'],
                    'file-type': f['file-type'].name,
                    'size': {
                        'size-type': f['size'][0].name,
                        'size-volume': f['size'][1]
                    }
                }
            })
        elif data_type == 'dir':
            # 디렉토리 정보 요청
            try:
                d: DirectoryData = STORAGE_MANAGER.get_dir_info(req_static_id, req)
                f_list, d_list = STORAGE_MANAGER.get_dirlist(req_static_id, req)

                # 디렉토리 안에 존재하는 파일 및 디렉토리 리스트 수집
                f_list_arr = [{'name': _f['file-name'], 'type': _f['file-type'].name} for _f in f_list]
                d_list_arr = [_d['dir-name'] for _d in d_list]

            except MicrocloudchipException as e:
                return JsonResponse({'code': e.errorCode})

            return JsonResponse({
                'code': 0,
                'data': {
                    'info': {
                        # Create Date와 Modify Date의 TimeFormat -> YYYY/MM/DD HH:MM:SS
                        'create-date': d['create-date'].strftime(TIME_FORMAT),
                        'modify-date': d['modify-date'].strftime(TIME_FORMAT),
                        'dir-name': d['dir-name'],
                        'file-size': d['file-size']
                    },
                    'list': {
                        'file': f_list_arr,
                        'dir': d_list_arr
                    }
                }
            })
        else:
            err = MicrocloudchipSystemAbnormalAccessError("Access Error")
            return JsonResponse({'code': err.errorCode})

    @check_token_in_class_view
    def patch(self, request: Request, data_type: str, static_id: str, root: str, req_static_id: str):
        # 파일 및 디렉토리 수정

        root: str = DataControlView.get_real_root(root)

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
                dir_name: str = data.get('dir-name')
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

    @check_token_in_class_view
    def delete(self, request: Request, data_type: str, static_id: str, root: str, req_static_id: str):

        root: str = DataControlView.get_real_root(root)

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
