from module.MicrocloudchipException.exceptions import MicrocloudchipAuthAccessError, \
    MicrocloudchipStorageOverCapacityError
from module.data_builder.directory_builder import DirectoryBuilder
from module.data_builder.file_builder import FileBuilder
from module.label.file_type import FileVolumeType
from module.manager.user_manager import UserManager
from module.manager.worker_manager import WorkerManager
from module.specification.System_config import SystemConfig

import os


class StorageManager(WorkerManager):

    def __new__(cls, config: SystemConfig):
        if not hasattr(cls, 'user_manager_instance'):
            cls.instance = super(WorkerManager, cls).__new__(cls)
        return cls.instance

    def __get_user_root(self, static_id: str) -> str:
        return os.path.join(self.config.get_system_root(), 'storage', static_id, 'root')

    def upload_file(
            self,
            req_static_id: str,
            req: dict,
            user_manager: UserManager
    ):
        # 다른 사용자가 파일을 컨트롤 해선 안된다.
        try:
            target_static_id: str = req['static-id']
            target_root: str = req['target-root']
            raw_data: bytes = req['raw-data']
        except IndexError as e:
            raise e

        # 권한 체크
        if req_static_id != target_static_id:
            raise MicrocloudchipAuthAccessError("Auth Failed to access upload file")

        # 용량 체크
        user_info = user_manager.get_user_by_static_id(target_static_id)

        available_storage: tuple = FileVolumeType.sub(user_info['volume_type'].to_tuple(),
                                                      user_manager.get_used_size(target_static_id))
        available_storage = \
            FileVolumeType.sub(available_storage, FileVolumeType.get_file_volume_type(len(raw_data)))
        if available_storage[1] < 0:
            raise MicrocloudchipStorageOverCapacityError("Storage Capacity overflow")

        # 업로드
        # 이 단계에서 발생한 예외들은 바로 송출
        try:
            file_builder = FileBuilder()
            file_builder.set_system_root(self.config.get_system_root()) \
                .set_author_static_id(target_static_id) \
                .set_target_root(target_root) \
                .set_raw_data(raw_data).save()
        except Exception as e:
            raise e

    def generate_directory(
            self,
            req_static_id: str,
            req: dict
    ):
        try:
            target_static_id: str = req['static-id']
            target_root: str = req['target-root']
        except IndexError as e:
            raise e

        # 권한 체크
        if req_static_id != target_static_id:
            raise MicrocloudchipAuthAccessError("Auth failed to access generate directory")

        # 디렉토리 생성
        try:
            directory_builder: DirectoryBuilder = DirectoryBuilder()
            directory_builder.set_system_root(self.config.get_system_root()) \
                .set_author_static_id(target_static_id) \
                .set_target_root(target_root).save()
        except Exception as e:
            raise e