import sys
from abc import ABCMeta

from module.specification.System_config import SystemConfig


class Manager(metaclass=ABCMeta):
    config: SystemConfig
    TOKEN: str = '\\' if sys.platform == "win32" else "/"

    def __init__(self, config: SystemConfig):
        self.config = config
