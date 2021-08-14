from abc import ABC
import os

from module.MicrocloudchipException.exceptions import MicrocloudchipDirectoryAlreadyExistError
from module.data_builder.storage_builder import StorageBuilder


class DirectoryBuilder(StorageBuilder, ABC):
    """
        디렉토리 생성 및 삭제 Builder
    """

    def is_all_have(self) -> bool:
        if not self.system_root or not self.target_root or \
                not self.TOKEN or not self.author_static_id:
            return False
        return True

    def get_full_root(self) -> str:
        if self.is_all_have():
            return f"{self.system_root}{self.TOKEN}storage" \
                   f"{self.TOKEN}{self.author_static_id}{self.TOKEN}root{self.TOKEN}" \
                   f"{self.target_root}"
        raise ValueError("All data is not filled")

    def save(self):
        try:
            full_root = self.get_full_root()
        except ValueError as e:
            raise e
        if os.path.isdir(full_root):
            # 이미 존재한 경우
            raise MicrocloudchipDirectoryAlreadyExistError(f"Directory {self.target_root} already exist")
        else:
            os.mkdir(full_root)
