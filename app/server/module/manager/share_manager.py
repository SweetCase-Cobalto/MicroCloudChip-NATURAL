import time

from module.MicrocloudchipException.exceptions import *
from module.data.shared_storage_data import SharedFileData
from module.data_builder.shared_storage_builder import SharedFileBuilder
from module.manager.internal_database_concurrency_manager import InternalDatabaseConcurrencyManager
from module.manager.worker_manager import WorkerManager
from module.specification.System_config import SystemConfig
import datetime
import app.models as model
import heapq
from typing import List
import threading


class ShareManager(WorkerManager):
    time_limit: datetime.timedelta
    thread_sleep_long: float = 1 / 1_000
    shared_monitoring_thread: threading.Thread

    def __new__(cls, config: SystemConfig,
                time_limit: datetime.timedelta = datetime.timedelta(days=30)):
        # Singletone 방식
        if not hasattr(cls, 'share_manager_instance'):
            cls.share_manager_instance = super(ShareManager, cls).__new__(cls)
        return cls.share_manager_instance

    def __init__(self, system_config: SystemConfig,
                 time_limit: datetime.timedelta = datetime.timedelta(days=30)):
        # Default timedelta 값은 30일

        super().__init__(system_config)
        self.time_limit = time_limit

        # shared thread monitoring 진행
        self.shared_monitoring_thread = threading.Thread(target=self.__thread_process)
        self.shared_monitoring_thread.daemon = True
        self.shared_monitoring_thread.start()

    def get_shared_id(self, target_static_id: str, target_root: str) -> str:
        """ File Root와 User id로 shared id 찾기"""
        try:
            sfd: SharedFileData = SharedFileData(self.config.get_system_root(), target_static_id, target_root)()
            return sfd.shared_id
        except MicrocloudchipException:
            return None

    def share_file(
            self,
            req_static_id: str,
            target_static_id: str,
            target_root: str):
        """Share File

        """
        if req_static_id != target_static_id:
            raise MicrocloudchipAuthAccessError("Only One User can shared")

        try:
            self.process_locker.acquire()
            SharedFileBuilder().set_system_root(self.config.get_system_root()) \
                .set_author_static_id(target_static_id) \
                .set_target_root(target_root).save()
        except MicrocloudchipException as e:
            self.process_locker.release()
            raise e
        except Exception as e:
            # MicrocloudchipException이 아닌 내부 에러
            self.process_locker.release()
            raise MicrocloudchipSystemInternalException(e)
        else:
            self.process_locker.release()

    def unshare_file(
            self,
            req_static_id: str,
            target_static_id: str,
            target_shared_id: str
    ):
        """Unshare file"""

        if req_static_id != target_static_id:
            raise MicrocloudchipAuthAccessError("Only One User can shared")

        try:
            self.process_locker.acquire()
            SharedFileData(shared_id=target_shared_id, system_root=self.config.system_root)().unshare()
        except MicrocloudchipException as e:
            self.process_locker.release()
            raise e
        else:
            self.process_locker.release()

    def download_shared_file(self, target_shared_id: str) -> str:
        # Raw File Root를 반환한다.
        try:
            self.process_locker.acquire()
            s = str(SharedFileData(system_root=self.config.system_root, shared_id=target_shared_id)())
            self.process_locker.release()
            return s
        except MicrocloudchipException as e:
            self.process_locker.release()
            raise e

    def change_shared_file_root(self, target_shared_id: str, new_root: str) -> str:
        # 파일 명 변경 및 루트 변경
        # StorageManager 안에서 작동해야 하며 절대 단독으로 사용하지 말 것
        try:
            self.process_locker.acquire()
            sf: SharedFileData = SharedFileData(shared_id=target_shared_id, system_root=self.config.system_root)()
            sf.update_root(new_root)
            self.process_locker.release()

        except MicrocloudchipException as e:
            self.process_locker.release()
            raise e

    def change_shared_file_root_by_changed_directory(self, user_static_id: str,
                                                     from_directory: str, new_directory: str):
        # 절대 단독으로 사용하지 말고 storage manager에서 변경 수행을 끝낸 다음에 사용할 것
        SharedFileData.change_file_root_by_changed_directory(user_static_id, from_directory, new_directory)

    def __thread_process(self):
        # Application Sub Thread

        # 만료 대상 Shared File List (Heap)
        expired_shareds: List[(str, model.SharedFile)] = []

        thread_timers = {"refreshed-time": datetime.datetime.now(), "is-first": True}
        if self.time_limit >= datetime.timedelta(days=1):
            # 1일 이상일 경우 1일로 측정
            thread_timers['time-delta'] = datetime.timedelta(days=1)
        else:
            # 1일 이하일 경우 유효기간의 10일로 책정
            thread_timers['time-delta'] = self.time_limit / 10

        # 다음 새로고침 대상 시간
        # 처음엔 바로 작동해야 하므로 now로 설정
        thread_timers['next-refresh-time'] = thread_timers['refreshed-time']

        # Task Functions
        def refresh():

            # timer update
            thread_timers["refreshed-time"] = datetime.datetime.now()
            thread_timers['time-delta'] = datetime.timedelta(days=1) if self.time_limit >= datetime.timedelta(days=1) \
                else self.time_limit / 10
            thread_timers['next-refresh-time'] = thread_timers['refreshed-time'] + thread_timers['time-delta']

            # 다음 리프레시 시간 전에 만료될 Shared File 갖고오기
            self.process_locker.acquire()
            try:
                end_time = thread_timers['refreshed-time'] + thread_timers['time-delta'] - self.time_limit

                expired_list: List[model.SharedFile] = \
                    SharedFileData.get_shared_file_for_shared_manager_queue(
                        self.config.get_system_root(), end_time)

            except Exception as e:
                self.process_locker.release()
                raise e
            else:
                if self.process_locker.locked():
                    self.process_locker.release()
            while expired_list:
                expired_data: model.SharedFile = expired_list.pop()

                # 일찍 만료되는 순으로 정렬
                heapq.heappush(expired_shareds, (expired_data.start_date + self.time_limit, expired_data.shared_id))

        while True:
            now: datetime.datetime = datetime.datetime.now()

            # Refresh 타임 측정 및 진행
            if now >= thread_timers['next-refresh-time']:
                try:
                    refresh()
                except Exception as e:
                    raise e
            else:
                # 만료 모니터링
                if expired_shareds:
                    if expired_shareds[-1][0] < now:
                        # 만료되었음
                        _, shared_id = heapq.heappop(expired_shareds)
                        try:
                            shared_data = SharedFileData(shared_id=shared_id, system_root=self.config.system_root)()
                            shared_data.unshare()
                        except MicrocloudchipException:
                            pass

            time.sleep(self.thread_sleep_long)
