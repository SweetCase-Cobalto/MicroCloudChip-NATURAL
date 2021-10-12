import datetime

from module.manager.manager import Manager
from module.manager.worker_manager import WorkerManager
from module.specification.System_config import SystemConfig


class InternalDatabaseConcurrencyManager(WorkerManager):
    """ SQLite로 실행할 경우
        동시에 DB접근을 할 수 없는데 DJango 내에서
        이를 컨트롤을 못하기 때문에 동시성을 관리하는
        데이터베이스 병행성 관리자 클래스 생성

        모든 함수는 Decorator로 작동시켜야 한다
    """

    def __new__(cls, config: SystemConfig):
        # Singletone 기법으로 작동한다.
        if not hasattr(cls, 'database_concurrency_manager_instance'):
            cls.database_concurrency_manager_instance = \
                super(InternalDatabaseConcurrencyManager, cls).__new__(cls)
        return cls.database_concurrency_manager_instance

    def __init__(self, system_config: SystemConfig):
        super().__init__(system_config)

    def lock_db_process(self):
        if self.config.rdbms_type == SystemConfig.INTERNAL:
            # SQLite일 경우만 동작한다
            self.process_locker.acquire()

    def unlock_db_process(self):
        if self.config.rdbms_type == SystemConfig.INTERNAL and self.process_locker.locked():
            self.process_locker.release()

    def manage_internal_transaction(self, func):
        # decoratro function
        lock = self.lock_db_process
        unlock = self.unlock_db_process

        def wrapper(instance: object, *args, **kwargs):
            result = None
            try:
                lock()
                result = func(instance, *args, **kwargs)
            except Exception as e:
                unlock()
                raise e
            else:
                unlock()
                return result

        return wrapper
