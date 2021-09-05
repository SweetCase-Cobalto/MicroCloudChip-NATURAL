from django.http import JsonResponse, HttpResponse

from rest_framework.decorators import api_view
from rest_framework.request import Request

from app.views.custom_decorators import check_token


@check_token
@api_view(['GET'])
def view_download_single_object(request: Request, data_type: str, static_id: str, root: str, req_static_id: str):
    return JsonResponse({'code': 0})
