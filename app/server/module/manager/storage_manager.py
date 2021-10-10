from module.MicrocloudchipException.exceptions import *
from module.data.storage_data import FileData, DirectoryData
from module.data_builder.directory_builder import DirectoryBuilder
from module.data_builder.file_builder import FileBuilder
from module.label.file_type import FileVolumeType
from module.manager.share_manager import ShareManager
from module.manager.worker_manager import WorkerManager
from module.specification.System_config import SystemConfig

import os
import stat
import datetime

import module.tools.zip as custom_zip


class StorageManager(WorkerManager):

    def __new__(cls, config: SystemConfig):
        # Singletone 방식
        if not hasattr(cls, 'user_manager_instance'):
            cls.instance = super(WorkerManager, cls).__new__(cls)
        return cls.instance

    def __get_user_root(self, static_id: str) -> str:
        # user root 구하기
        return os.path.join(self.config.get_system_root(), 'storage', static_id, 'root')

    def __get_user_tmp_root(self, static_id: str) -> str:
        # 파일을 추출하기 위한 임시 디렉토리 루트 구하기
        return os.path.join(self.config.get_system_root(), 'storage', static_id, 'tmp')

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
        user_info = user_manager.get_user_by_static_id(req_static_id, target_static_id)

        # 사용가능한 남아있는 용량
        available_storage: tuple = FileVolumeType.sub(user_info['volume-type'].to_tuple(),
                                                      user_manager.get_used_size(target_static_id))
        # 사용가능한 남아있는 욜양 - 업로드 될 파일 용량
        # 음수면 업로드가 불가하다.
        available_storage = \
            FileVolumeType.sub(available_storage, FileVolumeType.get_file_volume_type(len(raw_data)))
        if available_storage[1] < 0:
            # 용량 초과로 인한 업로드 불가
            raise MicrocloudchipStorageOverCapacityError("Storage Capacity overflow")

        # 업로드
        # 이 단계에서 발생한 예외들은 바로 송출
        try:
            # File Upload를 위한 Builder 생성 및 저장
            file_builder = FileBuilder()
            file_builder.set_system_root(self.config.get_system_root()) \
                .set_author_static_id(target_static_id) \
                .set_target_root(target_root) \
                .set_raw_data(raw_data).save()
        except Exception as e:
            raise e

    def get_file_info(self, req_static_id: str, req: dict) -> FileData:
        # File Information 갖고오기
        try:
            # req 데이터 추출
            target_static_id: str = req['static-id']
            target_root: str = req['target-root']
        except KeyError as e:
            raise e

        # 권한 체크
        if req_static_id != target_static_id:
            raise MicrocloudchipAuthAccessError("Auth failed to access update file")

        # 실제 파일 루트
        src_root: str = os.path.join(self.__get_user_root(target_static_id), target_root)
        try:
            # 파일 데이터 갖고오기
            f = FileData(src_root)()
        except MicrocloudchipException as e:
            raise e
        except Exception as e:
            raise e
        else:
            # 파일 정보 리턴
            return f

    def update_file(
            self,
            req_static_id: str,
            req: dict,
            share_manager: ShareManager
    ):
        # 파일 정보 수정(이름 수정)
        try:
            target_static_id: str = req['static-id']
            target_root: str = req['target-root']
            change_elements: dict = req['change']
        except KeyError as e:
            raise e

        # 권한 체크
        if req_static_id != target_static_id:
            raise MicrocloudchipAuthAccessError("Auth failed to access update file")

        # Target Root는 URL 상의 루트이므로 토큰(루트 토큰)을 바꾼다
        # 예를 들어 Windows Platform 일 경우 해당 루트가 aaa/bbb 이면 aaa\bbb로 변경한다
        __target_root = self.TOKEN.join(target_root.split('/'))

        # Raw Root
        src_root: str = os.path.join(self.__get_user_root(target_static_id), __target_root)

        try:
            # 파일 정보 검색
            f = FileData(src_root)()

            # 이름 바꾸기
            f.update_name(change_elements['name'])

            # Share 여부 판단 후 변경
            shared_id: str = share_manager.get_shared_id(target_static_id, target_root)
            if shared_id:
                # 되어있으면 변경
                share_manager.change_shared_file_root(shared_id, '/'.join(target_root.split('/')[:-1] + [f.name]))

        except MicrocloudchipException as e:
            raise e
        except Exception as e:
            raise e

    def generate_directory(
            self,
            req_static_id: str,
            req: dict
    ):
        # 디렉토리 만들기
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
            req: dict,
            share_manager: ShareManager
    ):
        # 디렉토리 정보 수정(이름 수정)
        try:
            target_static_id: str = req['static-id']
            target_root: str = req['target-root']
            change_elements: dict = req['change']
        except KeyError as e:
            raise e

        # 권한 체크
        if target_static_id != req_static_id:
            raise MicrocloudchipAuthAccessError("Auth failed to access generate directory")

        # Target Root는 URL 상의 루트이므로 토큰을 바꾼다
        # 예를 들어 Windows Platform 일 경우 해당 루트가 aaa/bbb 이면 aaa\bbb로 변경한다
        __target_root = self.TOKEN.join(target_root.split('/'))

        # 변경 대상 절대루트 생성
        src_root: str = os.path.join(self.__get_user_root(target_static_id), __target_root)

        # 업데이트
        try:
            d: DirectoryData = DirectoryData(src_root)()

            # 이름 바꾸기
            d.update_name(change_elements['name'])

            # Shared Data 내용도 바꾸기
            share_manager.change_shared_file_root_by_changed_directory(target_static_id, target_root, d.name)

        except MicrocloudchipException as e:
            raise e
        except Exception as e:
            # 기타 알수 없는 에러
            raise e

    def get_dir_info(self, req_static_id: str, req: dict):
        # 디렉토리 정보 얻기
        try:
            target_static_id = req['static-id']
            target_root = req['target-root']
        except KeyError as e:
            raise e

        # 권한 체크
        if target_static_id != req_static_id:
            raise MicrocloudchipAuthAccessError("Auth failed to access generate directory")

        # 디렉토리 루트
        full_root: str = os.path.join(self.__get_user_root(target_static_id), target_root)

        try:
            # 정보 갖고오기
            r: DirectoryData = DirectoryData(full_root)()
        except MicrocloudchipDirectoryNotFoundError as e:
            raise e
        else:
            return r

    def get_dirlist(self, req_static_id: str, req: dict):
        # 디렉토리 리스트 갖고오기
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

        # 실제 루트
        full_root: str = os.path.join(self.__get_user_root(target_static_id), self.TOKEN.join(target_root.split('/')))
        # full_root: str = os.path.join(self.__get_user_root(target_static_id), target_root)

        # 디렉토리 확인
        if not os.path.isdir(full_root):
            raise MicrocloudchipDirectoryNotFoundError("Directory is not exist")

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

    def delete_file(self, req_static_id: str, req: dict, shared_manager: ShareManager):
        # 파일 삭제
        try:
            target_static_id = req['static-id']
            target_root = req['target-root']
        except KeyError as e:
            raise e
        # 권한 체크
        if target_static_id != req_static_id:
            raise MicrocloudchipAuthAccessError("Auth failed to access generate directory")

        # 삭제 대상 실제 루트
        full_root: str = os.path.join(self.__get_user_root(target_static_id), target_root)
        # 파일 정보 확인하기
        try:
            f_stat: os.stat_result = os.stat(full_root)
            if not stat.S_ISREG(f_stat.st_mode):
                # 파일이 아닌 경우
                raise MicrocloudchipFileNotFoundError("This Data Is Not File")

        except FileNotFoundError:
            raise MicrocloudchipFileNotFoundError("Incorrect File root")

        # 데이터 정보 갖고오고 삭제하기
        try:

            # 공유가 걸려있는 경우 삭제

            shared_id: str = shared_manager.get_shared_id(target_static_id, target_root)
            if shared_id:
                shared_manager.unshare_file(req_static_id, target_static_id, shared_id)

            # 데이터 갖고오기
            file_data: FileData = FileData(full_root)()
            # 삭제
            file_data.remove()
        except Exception as e:
            # 에러 안일어나긴 하는데 혹시 모르니까
            raise e

    def delete_directory(self, req_static_id: str, req: dict, share_manager: ShareManager):

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
            raise MicrocloudchipDirectoryNotFoundError("Incorrect File Root")

        # BFS 방식으로 삭제
        try:

            stack = [target_root]

            while stack:
                r = stack[-1]

                # Full Real Root
                full_r = os.path.join(self.config.system_root, "storage",
                                      target_static_id, "root", self.TOKEN.join(r.split('/')))

                f_list, d_list = self.get_dirlist(req_static_id, {
                    "static-id": target_static_id,
                    'target-root': r
                })

                # 파일 부터 죄다 삭제
                for f in f_list:
                    self.delete_file(req_static_id, {
                        'static-id': target_static_id,
                        'target-root': f"{r}/{f.name}",
                    }, share_manager)

                # 파일을 전부 삭제하고 디렉토리가 없는 경우
                # 그냥 현재 디렉토리를 삭제한다
                if len(d_list) == 0:
                    stack.pop()
                    # get full root

                    deleted_d: DirectoryData = DirectoryData(full_r)()
                    deleted_d.remove()
                else:
                    # 루트 를 더하고 스택에 추가
                    # POP 을 하지 않는 이유는 모든 모든 디렉토리가 없는 경우 대해 한 번 더 함수를 실행해서
                    # 루트 자체를 삭제하기 위해
                    for d in d_list:
                        next_r = f"{r}/{d.name}"
                        stack.append(next_r)

        except Exception as e:
            raise e

    def download_objects(self, req_static_id: str, req: dict) -> tuple:
        # return: (결과 파일 루트, zip파일 여부)
        # zip 같은 경우 사용자 루트의 tmp 디렉토리에 저장한다.
        try:
            target_static_id: str = req['static-id']
            parent_root: str = req['parent-root']
            object_list: list[tuple] = req['object-list']
            """
                object_list_element = {
                    "object-name": "XXXXX",
                    "type": "dir" or "file"
                }
            """

        except KeyError as e:
            raise e

        # 권한 체크
        if target_static_id != req_static_id:
            raise MicrocloudchipAuthAccessError("Auth failed to access donwload file")

        # zip 파일로 출력될 파일 이름
        result_file_name: str = f"Microcloudchip-f{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}.zip"

        if not object_list or len(object_list) == 0:
            # 다운로드 대상의 Object가 없는 경우
            raise MicrocloudchipSystemAbnormalAccessError("Object is nothing")
        elif len(object_list) == 1:
            # 단일 파일 또는 디렉토리 인 경우
            obj = object_list[0]
            if obj['type'] == 'dir':
                # 디렉토리 인 경우
                # Full_Root를 구한 다음 Zip를 만든다.

                req_full_root: str = os.path.join(
                    self.__get_user_root(target_static_id),
                    parent_root,
                    obj['object-name'],
                )
                save_full_root: str = os.path.join(
                    self.__get_user_tmp_root(target_static_id),
                    result_file_name
                )
                # 디렉토리 확인
                try:
                    DirectoryData(req_full_root)()
                except MicrocloudchipException as e:
                    # 못찾음
                    raise e

                # Zip 파일
                custom_zip.zip_multiple([req_full_root], save_full_root)

                return save_full_root, True

            elif obj['type'] == 'file':
                # 파일인 경우
                # zip으로 묶지 않는다

                full_root: str = os.path.join(
                    self.__get_user_root(target_static_id),
                    parent_root,
                    obj['object-name']
                )

                try:
                    # 파일 찾기
                    FileData(full_root)()
                except MicrocloudchipException as e:
                    # 못찾음
                    raise e
                else:
                    # 찾음
                    return full_root, False
            else:
                raise MicrocloudchipSystemAbnormalAccessError("type of object is illeagal")
        else:
            # 두개 이상
            req_full_root_list: list[str] = []
            save_full_root: str = os.path.join(
                self.__get_user_tmp_root(target_static_id),
                result_file_name
            )

            # req full root list 채우기
            for obj in object_list:
                # 파일이 존재하지 않는 경우 패싱
                req_full_root: str = os.path.join(
                    self.__get_user_root(target_static_id),
                    parent_root,
                    obj['object-name']
                )
                req_full_root_list.append(req_full_root)

            # 작업 시작
            custom_zip.zip_multiple(req_full_root_list, save_full_root)

            return save_full_root, True
