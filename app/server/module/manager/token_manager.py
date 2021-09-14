from module.manager.worker_manager import WorkerManager
from module.specification.System_config import SystemConfig

import random
import string

import threading
import time
import jwt


class TokenManager(WorkerManager):
    time_limit: int
    user_table: dict
    token_checker_thread: threading.Thread

    def __new__(cls, config: SystemConfig, time_limit: int):
        if not hasattr(cls, 'user_manager_instance'):
            cls.instance = super(WorkerManager, cls).__new__(cls)
        return cls.instance

    def __init__(self, system_config: SystemConfig, time_limit: int):
        super().__init__(system_config)

        # 초 단위
        self.time_limit = time_limit
        self.user_table = {}
        """
            key: JWT Token
            value: {'start': start_time, key: 복호화 키}
        """

        # 쓰레드 작동
        self.token_checker_thread = threading.Thread(target=self.__thread_work)
        self.token_checker_thread.daemon = True
        self.token_checker_thread.start()

    def __thread_work(self):
        # 멀티스레드 동작으로
        # 해당 토큰이 기한 이상이면 삭제
        while True:
            time.sleep(1 / 10 ** 3)  # 1 milliseconds

            self.process_locker.acquire()
            tokens = list(self.user_table.keys())
            for token in tokens:
                if time.time() - self.user_table[token]['start'] >= self.time_limit:
                    # 시간 초과될 경우 처리
                    try:
                        del self.user_table[token]
                    except KeyError:
                        pass
            self.process_locker.release()

    def login(self, user_static_id: str) -> str:

        # 랜덤 Key 생성
        def generate_key() -> str:
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

        self.process_locker.acquire()
        # 토큰 발급 시작
        k: str = generate_key()
        token: str = jwt.encode({"user-static-id": user_static_id}, k, algorithm='HS256')
        # User Table에 Token 추가
        self.user_table[token] = {
            "key": k,
            "start": time.time()
        }
        # 토큰 발급 끝
        self.process_locker.release()

        return token

    def __update_token(self, token: str):
        # 토큰 기한 갱신
        if token in self.user_table:
            self.process_locker.acquire()
            self.user_table[token]['start'] = time.time()
            self.process_locker.release()

    def is_logined(self, token: str) -> str:
        # 로그인이 되어있는 지 확인
        # 로그인이 되어있으면 static id를 반환한다.
        if token not in self.user_table:
            return None

        self.__update_token(token)

        # Decoding 후 static_id 전송
        static_id: str = jwt.decode(token, self.user_table[token]['key'], algorithms='HS256')["user-static-id"]
        return static_id

    def logout(self, token: str):
        # 로그아웃
        if token in self.user_table:
            self.process_locker.acquire()
            del self.user_table[token]
            self.process_locker.release()
