from module.MicrocloudchipException.exceptions import MicrocloudchipAuthAccessError, \
    MicrocloudchipStorageOverCapacityError, MicrocloudchipFileAlreadyExistError, MicrocloudchipFileNotFoundError, \
    MicrocloudchipFileAndDirectoryValidateError, MicrocloudchipDirectoryAlreadyExistError, \
    MicrocloudchipDirectoryNotFoundError
from module.data.storage_data import FileData, DirectoryData
from module.data_builder.directory_builder import DirectoryBuilder
from module.data_builder.file_builder import FileBuilder
from module.label.file_type import FileVolumeType
from module.manager.worker_manager import WorkerManager
from module.specification.System_config import SystemConfig

import os
import stat


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
            user_manager  # 이거 UserManager 인데 Import Recursive 문제로 힌트 표기 안함
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

            # 이름 바꾸기
            f.update_name(change_elements['name'])

        except (MicrocloudchipFileNotFoundError, MicrocloudchipFileAndDirectoryValidateError) as e:
            # 파일을 찾지 못한 경우, 파일 명이 유효하지 않은 경우
            raise e
        except ValueError:
            # 동일한 이름으로 저장하려는 경우
            raise MicrocloudchipAuthAccessError("Same name does not be changeable")
        except MicrocloudchipFileAlreadyExistError as e:
            # 파일 이름 변경 실패
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
            directory_builder: DirectoryBuilder = DirectoryBuilder()
            directory_builder.set_system_root(self.config.get_system_root()) \
                .set_author_static_id(target_static_id) \
                .set_target_root(target_root).save()
        except Exception as e:
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

            # 이름 바꾸기
            d.update_name(change_elements['name'])

        except MicrocloudchipFileNotFoundError as e:
            # 파일을 찾지 못한 경우, 파일 명이 유효하지 않은 경우
            raise e
        except ValueError:
            # 동일한 이름으로 저장하려는 경우
            raise MicrocloudchipAuthAccessError("Same name does not be changeable")
        except (MicrocloudchipDirectoryAlreadyExistError, MicrocloudchipFileAndDirectoryValidateError) as e:
            # 파일 이름 변경 실패, 파일명 유효하지 않음
            raise e
        except Exception as e:
            # 기타 알수 없는 에러
            raise e

    def get_data(self, req_static_id: str, req: dict):
        try:
            target_static_id = req['static-id']
            target_root = req['target-root']
        except KeyError as e:
            raise e

        # 권한 체크
        if target_static_id != req_static_id:
            raise MicrocloudchipAuthAccessError("Auth failed to access generate directory")

        # 데이터 갖고오기
        f_list: list[FileData] = []
        d_list: list[DirectoryData] = []

        full_root: str = os.path.join(self.__get_user_root(target_static_id), target_root)

        try:

            # 헌재 디렉토리에서 검색된 파일 및 디렉토리 순환 조사
            # full_root 의 데이터가 없으면 FileNotFoundError
            for f_name in os.listdir(full_root):

                f_root: str = os.path.join(full_root, f_name)
                f_stat: os.stat_result = os.stat(f_root)

                # 파일/디렉토리 확인
                if stat.S_ISDIR(f_stat.st_mode):
                    d_list.append(DirectoryData(f_root)())
                elif stat.S_ISREG(f_stat.st_mode):
                    f_list.append(FileData(f_root)())

        except FileNotFoundError:
            raise MicrocloudchipAuthAccessError("Incorrect File root")

        return f_list, d_list

    def delete_file(self, req_static_id: str, req: dict):

        try:
            target_static_id = req['static-id']
            target_root = req['target-root']
        except KeyError as e:
            raise e

        # 권한 체크
        if target_static_id != req_static_id:
            raise MicrocloudchipAuthAccessError("Auth failed to access generate directory")

        full_root: str = os.path.join(self.__get_user_root(target_static_id), target_root)

        # 파일 정보 확인하기
        try:
            f_stat: os.stat_result = os.stat(full_root)
            if not stat.S_ISREG(f_stat.st_mode):
                # 파일이 아닌 경우
                raise MicrocloudchipFileNotFoundError("This Data Is Not File")

        except FileNotFoundError:
            raise MicrocloudchipAuthAccessError("Incorrect File root")

        # 데이터 정보 갖고오고 삭제하기
        try:
            # 데이터 갖고오기
            file_data: FileData = FileData(full_root)()
            # 삭제
            file_data.remove()
        except Exception as e:
            # 에러 안일어나긴 하는데 혹시 모르니까
            raise e

    def delete_directory(self, req_static_id: str, req: dict):

        # 데이터 체크
        try:
            target_static_id = req['static-id']
            target_root = req['target-root']
        except KeyError as e:
            raise e

        # 권한 체크
        if target_static_id != req_static_id:
            raise MicrocloudchipAuthAccessError("Auth failed to access generate directory")

        full_root: str = os.path.join(self.__get_user_root(target_static_id), target_root)

        # 디렉토리 확인
        try:
            d_stat: os.stat_result = os.stat(full_root)
            if not stat.S_ISDIR(d_stat.st_mode):
                raise MicrocloudchipDirectoryNotFoundError("This Data is not Directory")
        except FileNotFoundError:
            raise MicrocloudchipAuthAccessError("Incorrect File Root")

        # BFS 방식으로 삭제
        try:

            stack = [full_root]

            while stack:
                r = stack[-1]

                f_list, d_list = self.get_data(req_static_id, {
                    "static-id": target_static_id,
                    'target-root': r
                })

                # 파일 부터 죄다 삭제
                for f in f_list:
                    self.delete_file(req_static_id, {
                        'static-id': target_static_id,
                        'target-root': os.path.join(r, f.name)
                    })

                # 파일을 전부 삭제하고 디렉토리가 없는 경우
                # 그냥 현재 디렉토리를 삭제한다
                if len(d_list) == 0:
                    stack.pop()
                    deleted_d: DirectoryData = DirectoryData(r)()
                    deleted_d.remove()
                else:
                    # 루트 를 더하고 스택에 추가
                    # POP 을 하지 않는 이유는 모든 모든 디렉토리가 없는 경우 대해 한 번 더 함수를 실행해서
                    # 루트 자체를 삭제하기 위해
                    for d in d_list:
                        next_r = os.path.join(r, d.name)
                        stack.append(next_r)

        except Exception as e:
            raise e
