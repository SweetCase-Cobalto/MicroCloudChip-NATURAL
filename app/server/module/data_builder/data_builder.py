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
        pass
