import os

from django.http import JsonResponse, HttpResponse

from rest_framework.decorators import api_view
from rest_framework.request import Request

from app.views.custom_decorators import check_token
from app.views.data_control_view import DataControlView
from module.MicrocloudchipException.base_exception import MicrocloudchipException
from module.MicrocloudchipException.exceptions import MicrocloudchipSystemAbnormalAccessError

import mimetypes

from . import *


@check_token
@api_view(['GET'])
def view_download_single_object(
        request: Request,
        data_type: str,
        static_id: str,
        root: str,
        req_static_id: str) -> HttpResponse:
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
        with open(result_file_root, 'rb') as f:
            content_type, _ = mimetypes.guess_type(result_file_root)
            response = HttpResponse(f, content_type=content_type)

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
        req_static_id: str) -> HttpResponse:

    print(request.GET)

    return JsonResponse({'code': 0})
