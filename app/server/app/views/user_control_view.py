from django.http import JsonResponse
from django.views import View
from rest_framework.request import Request


class UserControlView(View):

    def put(self, request: Request, static_id: str):
        # 데이터 수정
        print("checked")
        print(static_id)

        return JsonResponse({"ok": "ok"})
