from module.MicrocloudchipException.exceptions import MicrocloudchipAuthAccessError, \
    MicrocloudchipStorageOverCapacityError, MicrocloudchipFileAlreadyExistError, MicrocloudchipFileNotFoundError, \
    MicrocloudchipFileAndDirectoryValidateError, MicrocloudchipDirectoryAlreadyExistError
from module.data.storage_data import FileData, DirectoryData
from module.data_builder.directory_builder import DirectoryBuilder
from module.data_builder.file_builder import FileBuilder
from module.label.file_type import FileVolumeType
from module.manager.user_manager import UserManager
from module.manager.worker_manager import WorkerManager
from module.specification.System_config import SystemConfig

import os

from module.validator.storage_validator import StorageValidator


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
            self.process_locker.acquire()

            file_builder = FileBuilder()
            file_builder.set_system_root(self.config.get_system_root()) \
                .set_author_static_id(target_static_id) \
                .set_target_root(target_root) \
                .set_raw_data(raw_data).save()

            self.process_locker.release()

        except Exception as e:
            self.process_locker.release()
            raise e

    def update_file(
            self,
            req_static_id: str,
            req: dict,
    ):

        try:
            target_static_id: str = req['static-id']
            target_root: str = req['target-root']
            change_elements: dict = req['change']
        except KeyError as e:
            raise e

        # 권한 체크
        if req_static_id != target_static_id:
            raise MicrocloudchipAuthAccessError("Auth failed to access update file")

        src_root: str = os.path.join(self.__get_user_root(target_static_id), target_root)

        try:
            # 파일 정보 검색
            f = FileData(src_root)()

            self.process_locker.acquire()
            # 이름 바꾸기
            f.update_name(change_elements['name'])
            self.process_locker.release()

        except (MicrocloudchipFileNotFoundError, MicrocloudchipFileAndDirectoryValidateError) as e:
            # 파일을 찾지 못한 경우, 파일 명이 유효하지 않은 경우
            raise e
        except ValueError:
            # 동일한 이름으로 저장하려는 경우
            raise MicrocloudchipAuthAccessError("Same name does not be changeable")
        except MicrocloudchipFileAlreadyExistError as e:
            # 파일 이름 변경 실패
            self.process_locker.release()
            raise e
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
            self.process_locker.acquire()
            directory_builder: DirectoryBuilder = DirectoryBuilder()
            directory_builder.set_system_root(self.config.get_system_root()) \
                .set_author_static_id(target_static_id) \
                .set_target_root(target_root).save()
            self.process_locker.release()
        except Exception as e:
            self.process_locker.release()
            raise e

    def update_directory(
            self,
            req_static_id: str,
            req: dict
    ):

        try:
            target_static_id: str = req['static-id']
            target_root: str = req['target-root']
            change_elements: dict = req['change']
        except KeyError as e:
            raise e

        # 권한 체크
        if target_static_id != req_static_id:
            raise MicrocloudchipAuthAccessError("Auth failed to access generate directory")

        # 변경 대상 절대루트 생성
        src_root: str = os.path.join(self.__get_user_root(target_static_id), target_root)

        # 업데이트
        try:
            d: DirectoryData = DirectoryData(src_root)()

            self.process_locker.acquire()
            d.update_name(change_elements['name'])
            self.process_locker.release()

        except MicrocloudchipFileNotFoundError as e:
            # 파일을 찾지 못한 경우, 파일 명이 유효하지 않은 경우
            raise e
        except ValueError:
            # 동일한 이름으로 저장하려는 경우
            raise MicrocloudchipAuthAccessError("Same name does not be changeable")
        except (MicrocloudchipDirectoryAlreadyExistError, MicrocloudchipFileAndDirectoryValidateError) as e:
            # 파일 이름 변경 실패, 파일명 유효하지 않음
            self.process_locker.release()
            raise e
        except Exception as e:
            raise e
