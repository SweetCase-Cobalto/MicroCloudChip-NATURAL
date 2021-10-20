import mimetypes

from django.http import JsonResponse, HttpResponse
from rest_framework.request import Request
from rest_framework.views import APIView
from module.MicrocloudchipException.exceptions import *
from . import *

import os

from .custom_decorators import check_token_in_class_view


class SharedFileControlView(APIView):

    def get(self, request: Request, shared_id: str) -> HttpResponse:
        # 공유된 파일의 데이터 받아오기
        try:
            data = SHARE_MANAGER.download_shared_file(shared_id)
            filename, real_file_root = data
        except MicrocloudchipException as e:
            return JsonResponse({"code": e.errorCode})
        except Exception:
            err = MicrocloudchipSystemInternalException("Unknown Error")
            return JsonResponse({"code": err.errorCode})


        mode = None
        # mode -> raw => data (default)
        # mode -> info => information

        if "mode" in request.GET:
            mode = request.GET['mode']
        else:
            mode = "raw"
            
        # get real_file_root and download response
        if mode == "raw":
            if not os.path.isfile(real_file_root):
                # Check is file exist
                err = MicrocloudchipFileNotFoundError("File Not Found")
                return JsonResponse({"code": err.errorCode})

            with open(real_file_root, 'rb') as _f:
                content_type, _ = mimetypes.guess_type(real_file_root)
                response = HttpResponse(_f, content_type=content_type)

            return response
        else:
            return JsonResponse({"code": 0, "data": {"filename": filename}})

    @check_token_in_class_view
    def delete(self, request: Request, shared_id: str, req_static_id: str, updated_token: str):

        # shared id의 주인 찾기
        target_static_id: str = SHARE_MANAGER.get_user_id_by_shared_id(shared_id)

        if not target_static_id:
            # 해당 shared_id가 만료되었거나 올바른 Shared가 아님
            err = MicrocloudchipFileIsNotSharedError("This shared id is not shared or wrong str")
            return JsonResponse({"code": err.errorCode})

        err: MicrocloudchipException = None
        try:
            # 제거 시작
            SHARE_MANAGER.unshare_file(req_static_id, target_static_id, shared_id)
        except MicrocloudchipException as e:
            # Expected Exception
            err = e
        except Exception as e:
            # None Expected Exception
            err = MicrocloudchipSystemInternalException(f"Internal Exception: {type(e)}:{e}")
            print(err)
        else:
            # Success
            err = MicrocloudchipSucceed()
        finally:
            return JsonResponse({"code": err.errorCode})