from django.http import JsonResponse
from rest_framework.request import Request
from rest_framework.views import APIView
from module.MicrocloudchipException.exceptions import *
from module.session_control.session_control import is_logined_event


class DataControlView(APIView):

    @staticmethod
    def check_is_logined(request: Request):
        # 로그인 되어있는 지 체크
        if not is_logined_event(request):
            raise MicrocloudchipLoginConnectionExpireError("Login Expired")

    def post(self, request: Request, data_type: str, static_id: str, root: str):
        print(root)
        # 파일 및 디렉토리 업로드
        return JsonResponse({"code": 0})
