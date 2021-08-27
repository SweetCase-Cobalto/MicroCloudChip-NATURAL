import sys
from abc import ABCMeta, abstractmethod


class DataBuilder(metaclass=ABCMeta):
    TOKEN: str = '\\' if sys.platform == "win32" else '/'
    system_root: str

    def set_system_root(self, system_root: str):
        self.system_root = system_root
        return self

    @abstractmethod
    def is_all_have(self) -> bool:
        # 데이터를 생성하기 위한 모든 요소들이 갖추어져 있는 지 확인
        pass
