from abc import ABCMeta, abstractmethod


class MicrocloudchipData(metaclass=ABCMeta):
    is_called: bool

    @abstractmethod
    def __call__(self):
        pass