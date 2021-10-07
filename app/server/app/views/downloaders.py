from django.http import JsonResponse, HttpResponse, QueryDict

from rest_framework.decorators import api_view
from rest_framework.request import Request

from app.views.custom_decorators import check_token
from app.views.data_control_view import DataControlView
from module.MicrocloudchipException.base_exception import MicrocloudchipException
from module.MicrocloudchipException.exceptions import MicrocloudchipSystemAbnormalAccessError

import mimetypes
import os

from . import *


@check_token
@api_view(['GET'])
def view_download_single_object(
        request: Request,
        data_type: str,
        static_id: str,
        root: str,
        req_static_id: str,
        updated_token: str):
    # parent root 찾기
    splited_root: list[str] = DataControlView.get_real_root(root).split('/')
    parent_root: str = ""
    target_obj: str = splited_root[-1]
    if len(splited_root) > 1:
        parent_root = '/'.join(splited_root[:-1])

    # 다운로드 요청 데이터 작성
    req = {
        "static-id": static_id,
        "parent-root": parent_root,
        "object-list": [],
    }

    if data_type == 'dir':
        req['object-list'].append({
            "object-name": target_obj,
            'type': 'dir'
        })
    elif data_type == "file":
        req['object-list'].append({
            "object-name": target_obj,
            'type': 'file'
        })
    else:
        e = MicrocloudchipSystemAbnormalAccessError("type of object is illeagal")
        raise e

    # 요창
    try:
        result_file_root, is_zip = STORAGE_MANAGER.download_objects(req_static_id, req)

        f = open(result_file_root, mode='rb')

        content_type, _ = mimetypes.guess_type(result_file_root)
        response = HttpResponse(f, content_type=content_type)

        if is_zip:
            result_file_name: str = f'{result_file_root.split(os.sep)[-1]}.zip'
        else:
            result_file_name: str = f'{result_file_root.split(os.sep)[-1]}'
        response['Content-Disposition'] = f'attachment; filename={result_file_name}'

        # Zip파일일 경우 없애부리기
        if is_zip:
            os.remove(result_file_root)

        # 파일 HttpResponse 객체
        return response

    except MicrocloudchipException as e:
        return JsonResponse({'code': e.errorCode})


@check_token
@api_view(['GET'])
def view_download_multiple_object(
        request: Request,
        static_id: str,
        parent_root: str,
        req_static_id: str,
        updated_token: str) -> HttpResponse:
    # get param 갖고오기
    params: QueryDict = request.GET
    # root를 제외한 실제 Root 구하기
    __parent_root = DataControlView.get_real_root(parent_root)

    req = {
        'static-id': static_id,
        'parent-root': '',
        'object-list': []
    }
    for raw_obj_type, obj_name in params.items():
        # raw_obj_type --> [OBJ TYPE]-[NUM]
        __splited = raw_obj_type.split('-')

        if len(__splited) != 2:
            e = MicrocloudchipSystemAbnormalAccessError("Parameter Error: key format")
            return JsonResponse({'code': e.errorCode})

        # file Type Checking
        if __splited[0] not in ['dir', 'file']:
            e = MicrocloudchipSystemAbnormalAccessError("Parameter Error: key type error")
            return JsonResponse({'code': e.errorCode})

        req['object-list'].append({
            'object-name': obj_name,
            'type': __splited[0]
        })

    try:
        # 작업 시작
        result_file_root, is_zip = STORAGE_MANAGER.download_objects(req_static_id, req)
    except MicrocloudchipException as e:
        return JsonResponse({'code': e.errorCode})
    with open(result_file_root, 'rb') as f:
        content_type, _ = mimetypes.guess_type(result_file_root)
        response = HttpResponse(f, content_type=content_type)

    # Zip파일일 경우 없애부리기 (원래 zip으로 저장되지만 만일을 대비해서)
    if is_zip:
        os.remove(result_file_root)

    return response


@check_token
@api_view(['GET'])
def view_download_user_icon(
        request: Request,
        static_id: str,
        req_static_id: str,
        updated_token: str
) -> HttpResponse:
    # Get Raw Asset Directory
    raw_root: str = os.path.join(SYSTEM_CONFIG.get_system_root(), 'storage', static_id, 'asset')

    # File Check
    if not os.path.isdir(raw_root):
        # 해당 디렉토리가 존재하지 않는 경우
        e = MicrocloudchipSystemAbnormalAccessError("This root is not exist")

        return JsonResponse({"code": e.errorCode})

    # is file Exist
    target: str = None
    for f in os.listdir(raw_root):
        # user icon image 찾기
        splited_f: list[str] = f.split('.')
        if len(splited_f) == 2 and \
                splited_f[0] == 'user' and splited_f[1] in ['jpg', 'png']:
            target = f
            break

    # icon이 존재하지 않는 경우
    if not target:
        e = MicrocloudchipSystemAbnormalAccessError("Image Not Found")
        return JsonResponse({"code": e.errorCode})

    # Image Data 출력
    raw_root = os.path.join(raw_root, target)
    with open(raw_root, 'rb') as f:
        content_type, _ = mimetypes.guess_type(raw_root)
        response = HttpResponse(f, content_type=content_type)
    return response
