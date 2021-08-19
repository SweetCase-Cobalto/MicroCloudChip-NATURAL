from abc import ABCMeta
from module.manager.manager import Manager
import threading

from module.specification.System_config import SystemConfig


class WorkerManager(Manager, metaclass=ABCMeta):

    # 하니의 인스턴스로 작동하고
    # 모든 작업은 하나의 인스턴스가 관리한다
    # 따라서 작업을 제어할 Lock 이 필요하다
    # __new__ Function 은 상속이 안될거 같아서 가장 하단의 클래스가 대신 작성한다.
    process_locker: threading.Lock = threading.Lock()

    def __init__(self, system_config: SystemConfig):
        super().__init__(system_config)
