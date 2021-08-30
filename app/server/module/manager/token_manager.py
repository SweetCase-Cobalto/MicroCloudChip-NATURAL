from module.manager.worker_manager import WorkerManager
from module.specification.System_config import SystemConfig

import time
import random
import string


class TokenManager(WorkerManager):
    time_limit: int
    user_table: dict

    def __new__(cls, config: SystemConfig, time_limit: int):
        if not hasattr(cls, 'user_manager_instance'):
            cls.instance = super(WorkerManager, cls).__new__(cls)
        return cls.instance

    def __init__(self, system_config: SystemConfig, time_limit: int):
        super().__init__(system_config)

        # 초 단위
        self.time_limit = time_limit

    def login(self, user_static_id: str) -> str:

        # 랜덤 토큰 생성
        def generate_token() -> str:
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

        while True:
            t: str = generate_token()
            if t not in self.user_table:
                new_token = t
                break

        self.user_table[new_token] = {
            "user-static-id": user_static_id,
            "start": time.time()
        }

        return new_token

    def __update_token(self, token: str):
        if token in self.user_table:
            self.user_table[token]['start'] = time.time()

    def is_logined(self, token: str) -> bool:
        if token in self.user_table:
            if time.time() - self.user_table[token]['start'] >= self.time_limit:
                del self.user_table[token]
                return False
            else:
                self.user_table[token]['start'] = time.time()
                return True
        else:
            return False

    def logout(self, token: str):
        if token in self.user_table:
            del self.user_table[token]
