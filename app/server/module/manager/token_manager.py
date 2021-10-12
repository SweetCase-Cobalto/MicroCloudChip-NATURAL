from module.manager.worker_manager import WorkerManager
from module.specification.System_config import SystemConfig
from module.MicrocloudchipException.exceptions import *

import random
import string
import datetime

import jwt


class TokenManager(WorkerManager):

    time_limit: datetime.timedelta
    token_key: str
    TIME_FORMAT: str = "%m/%d/%Y-%H:%M:%S"
    TOKEN_METHOD: str = "HS256"

    def __new__(cls, config: SystemConfig, time_limit: int):
        if not hasattr(cls, 'token_manager_instance'):
            cls.token_manager_instance = super(TokenManager, cls).__new__(cls)
        return cls.token_manager_instance

    def __init__(self, system_config: SystemConfig, time_limit: int):
        super().__init__(system_config)

        # 초 단위
        self.time_limit = datetime.timedelta(seconds=time_limit)

        # token key 생성
        def __generate_key() -> str:
            alphabet = string.ascii_lowercase
            numbers = '1234567890'

            new_token: str = ""
            for _ in range(128):
                select = random.randint(0, 1)
                if select:
                    new_token += alphabet[random.randint(0, len(alphabet) - 1)]
                else:
                    new_token += alphabet[random.randint(0, len(numbers) - 1)]
            return new_token

        self.token_key = __generate_key()

    def login(self, user_static_id: str) -> str:
        # 토큰 발급
        info: dict = {
            "user-static-id": user_static_id,
            "start-time": datetime.datetime.now().strftime(self.TIME_FORMAT),
            "is-activate": True
        }
        token: str = jwt.encode(info, self.token_key, algorithm=self.TOKEN_METHOD)
        return token

    def is_logined(self, token: str) -> (str, str):
        pass
        # 로그인이 되어있는 지 확인
        # 로그인이 되어있으면 static id과 새로운 token을 반환한다.
        # 아닐 경우 (None, None)을 반환한다.

        try:

            # decode token
            info: dict = jwt.decode(token, self.token_key, algorithms=self.TOKEN_METHOD)
            static_id: str = info['user-static-id']
            is_activate: bool = info["is-activate"]

            start_time: datetime = \
                datetime.datetime.strptime(info['start-time'], self.TIME_FORMAT)

            # 예상 종료 시간
            expected_end_time = start_time + self.time_limit

            # 예상 종료 시간보다 현재 시간이 더 길거나 만료처리될 경우
            if datetime.datetime.now() > expected_end_time or not is_activate:
                return None, None

            # 만료가 아닌 경우 start time 업데이트된 토큰 반환
            info['start-time'] = datetime.datetime.now().strftime(self.TIME_FORMAT)
            new_token: str = \
                jwt.encode(info, self.token_key, algorithm=self.TOKEN_METHOD)

            return static_id, new_token

        except jwt.exceptions.PyJWTError as e:
            raise MicrocloudchipSystemAbnormalAccessError("Token is not valid: failed to decode token")
        except KeyError:
            # 디코딩은 됐는 데 이에 대한 데이터가 없음
            raise MicrocloudchipSystemAbnormalAccessError("Token data is not valid")

    def logout(self, token: str) -> str:
        # 디코딩이 안되어 있는 경우
        try:
            info: dict = jwt.decode(token, self.token_key, algorithms=self.TOKEN_METHOD)

            if set(info.keys()) != {"user-static-id", "start-time", "is-activate"}:
                raise KeyError("")

            # 만료 처리하고 token return
            info['is-activate'] = False

            return jwt.encode(info, self.token_key, algorithm=self.TOKEN_METHOD)

        except jwt.exceptions.PyJWTError:
            raise MicrocloudchipSystemAbnormalAccessError("Token is not valid: failed to decode token")
        except KeyError:
            # 디코딩은 됐는 데 이에 대한 데이터가 없음
            raise MicrocloudchipSystemAbnormalAccessError("Token data is not valid")
