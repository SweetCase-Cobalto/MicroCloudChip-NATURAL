from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.request import Request

from app.views.custom_decorators import check_token
from module.MicrocloudchipException.exceptions import *
from . import *

@check_token
@api_view(['POST'])
def view_share_file(request: Request, req_static_id: str, updated_token: str) -> JsonResponse:
    err: MicrocloudchipException = None
    res = {}

    target_file_root: str = ""
    try:
        # Find Parameter
        target_file_root = request.data['file-root']
    except KeyError as e:
        # Failed
        _e = MicrocloudchipSystemAbnormalAccessError("Access Failed")
        return JsonResponse({"code": _e.errorCode})

    try:
        SHARE_MANAGER.share_file(req_static_id, req_static_id, target_file_root)
    except MicrocloudchipException as e:
        # In exception
        err = e
    except Exception as e:
        # Out Exception
        err = MicrocloudchipSystemInternalException(f"Internal Exception: {e}")
        print(f"{type(e)}: {e}")
    else:
        # Succeed
        res['data'] = {"shared-id": SHARE_MANAGER.get_shared_id(req_static_id, target_file_root)}
        err = MicrocloudchipSucceed()
    finally:
        res['code'] = err.errorCode
        return JsonResponse(res)