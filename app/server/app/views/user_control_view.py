from typing import Any

from django import http
from django.http import JsonResponse
from rest_framework.request import Request
from rest_framework.views import APIView


class UserControlView(APIView):

    def patch(self, request: Request, static_id: str) -> JsonResponse:

        print(request.data)
        return JsonResponse({"code": 0})
