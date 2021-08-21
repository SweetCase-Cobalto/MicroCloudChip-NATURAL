from django.http import HttpResponse, JsonResponse
from . import USER_MANAGER, STORAGE_MANAGER

from rest_framework.decorators import api_view
from rest_framework.request import Request


@api_view(['POST'])
def view_user_login(request: Request) -> JsonResponse:

    return JsonResponse({
        "hello": "world"
    })