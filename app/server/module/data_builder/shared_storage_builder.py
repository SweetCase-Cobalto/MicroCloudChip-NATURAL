import os
import stat
from abc import abstractmethod
from typing import Set

import app.models as model
from module.MicrocloudchipException.exceptions import *
from module.data_builder.storage_builder import StorageBuilder


class SharedStorageBuilder(StorageBuilder):
    # 공유된 파일 및 디렉토리 빌더 클래스의 상위 클래스

    REQUESTED_BUILDER_ATTR: Set[str] = {'author_static_id', 'target_root', "system_root", "selected_root"}

    selected_root: str # 사용자가 설정한 루트 그대로

    def is_all_have(self) -> bool:
        return set(self.__dict__.keys()) == SharedStorageBuilder.REQUESTED_BUILDER_ATTR

    def set_target_root(self, target_root):
        super().set_target_root(target_root)
        self.selected_root = target_root
        return self

    @abstractmethod
    def save(self):
        pass


class SharedFileBuilder(SharedStorageBuilder):
    # 공유된 파일 클래스
    def save(self):
        # Check attributes
        try:
            # Get Full Root
            full_root: str = self.get_full_root()
        except MicrocloudchipFileAndDirectoryValidateError as e:
            raise e

        # Check is exist
        try:
            file_stat: os.stat_result = os.stat(full_root)
        except FileNotFoundError:
            raise MicrocloudchipFileNotFoundError(f"This File is not exist: {full_root}")

        # Check File Type
        if stat.S_ISREG(file_stat.st_mode):
            # is file

            # 이미 등록되어있는 지 확인하기
            if model.SharedFile.objects.filter(user_static_id=self.author_static_id) \
                    .filter(file_root=self.selected_root).exists():
                raise MicrocloudchipSharedFileAlreadyExistError(f"Shared File is aleady exist: {self.selected_root}")

            # Save to database
            model.SharedFile(
                user_static_id=model.User.objects.get(static_id=self.author_static_id),
                file_root=self.selected_root
            ).save()
        elif stat.S_ISDIR(file_stat.st_mode):
            # is dir
            raise MicrocloudchipDirectoryAlreadyExistError(f"Target Root is Directory: {full_root}")
        else:
            raise MicrocloudchipFileNotFoundError(f"This File is special file: {full_root}")


