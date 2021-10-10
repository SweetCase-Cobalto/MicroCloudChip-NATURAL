import os
import sys
from abc import abstractmethod
from typing import Dict, Optional, List

from django.db.models.query import QuerySet

from app.serializers import SharedFileSerializer
from module.data.microcloudchip_data import MicrocloudchipData
from datetime import datetime
from module.MicrocloudchipException.exceptions import *
import app.models as model


class SharedStorageData(MicrocloudchipData):
    start_date: datetime
    target_root: str
    static_id: str
    shared_id: str
    system_root: str

    def __init__(self, system_root):
        self.system_root = system_root

    @abstractmethod
    def __call__(self):
        pass


class SharedFileData(SharedStorageData):

    def __init__(self, system_root: str = None, static_id: str = None, target_root: str = None, shared_id: str = None):
        super().__init__(system_root)

        self.target_root = target_root
        self.static_id = static_id
        self.shared_id = shared_id
        self.is_called = False

    def __call__(self):
        try:
            sf: model.SharedFile = None
            # From Database
            if self.shared_id:
                # Shared id로 검색하는 경우
                sf = model.SharedFile.objects \
                    .get(shared_id=self.shared_id)

            elif self.static_id and self.target_root:
                # Static ID와 Target Root로 검색하는 경우
                sf = model.SharedFile.objects \
                    .get(user_static_id=self.static_id, file_root=self.target_root)
            else:
                # Get Error
                raise MicrocloudchipSystemInternalException("attr not setted")

            serial = SharedFileSerializer(sf)
            serial = serial.create()
            raw_data: Dict[Optional] = serial

            self.start_date = raw_data['start_date']
            self.shared_id = raw_data['shared_id']
            self.target_root = raw_data['file_root']
            self.static_id = raw_data['user_static_id']

            # Check is file exist
            # 데이터 변경 문제로 삭제
            """
            real_root: str = os.path.join(self.system_root, "storage", self.static_id, "root", self.target_root)
            if not os.path.isfile(real_root):
                # Unshare 처리
                self.is_called = True
                self.unshare()
                raise MicrocloudchipFileNotFoundError("File Is Not Exist")
            """

            self.is_called = True
            return self

        except Exception:
            raise MicrocloudchipFileIsNotSharedError("This File is not shared")

    def unshare(self):
        self.__call__()
        if not self.is_called:
            raise MicrocloudchipDataFormatNotCalled("Data is not called yet")
        else:

            """
            data = SharedFileSerializer(data={"start_date": self.start_date,
                                              "user_static_id": self.static_id,
                                              "file_root": self.target_root,
                                              "shared_id": self.shared_id})

            data.build().delete()
            """

            model.SharedFile.objects.get(shared_id=self.shared_id).delete()
            self.is_called = False

    def update_root(self, new_root: str):
        # 파일 및 폴더 이름이 변경되었을 경우, 공유 상태를 유지하기 위해 사용
        if not self.is_called:
            raise MicrocloudchipDataFormatNotCalled("Data is not called yet")
        else:
            data: model.SharedFile = model.SharedFile.objects.get(shared_id=self.shared_id)
            data.file_root = new_root
            data.save()

    def __str__(self):
        # Real Root 출력
        if not self.is_called:
            return None
        t = '\\' if sys.platform == "win32" else "/"
        return os.path.join(self.system_root, "storage", self.static_id, "root",
                            t.join(self.target_root.split('/')))

    @staticmethod
    def init_shared_data_from_database(system_root: str, obj: model.SharedFile):
        # DB로부터 이미 갖고온 데이터로 ShareFileData 생성하기
        s: SharedFileData = SharedFileData(system_root=system_root, static_id=obj.user_static_id,
                                           target_root=obj.file_root, shared_id=obj.shared_id)
        s.start_date = obj.start_date
        s.is_called = True

        return s

    # Object Query
    @staticmethod
    def get_shared_file_for_shared_manager_queue(system_root: str, start_date: datetime) -> List:
        r = []
        for item in model.SharedFile.objects.filter(start_date__lte=start_date):
            r.append(SharedFileData.init_shared_data_from_database(system_root, item))
        return r

    @staticmethod
    def change_file_root_by_changed_directory(static_id: str, from_directory_root: str, new_directory_root: str):
        # 디렉토리 변경에 의해 공유된 데이터들의 루트도 같이 변경
        # Model로 직접 접근해서 수정
        # 절대 단독으로 쓰면 안되며 storage manager에서 directory 변경을 한 이후에 사용할 것

        def change_root(shared_file: model.SharedFile, new_directory_root) -> str:
            splited_cur_root: List[str] = shared_file.file_root.split('/')
            dir_root, file_name = '/'.join(splited_cur_root[:-1]), splited_cur_root[-1]
            # change dir_root
            dir_root = new_directory_root
            # paste full root
            full_root = f"{dir_root}/{file_name}"
            return full_root

        changed_list: QuerySet = model.SharedFile.objects.select_for_update() \
            .filter(user_static_id=static_id, file_root__iregex=rf'^{from_directory_root}/')

        for entry in changed_list:
            entry.file_root = change_root(entry, new_directory_root)
            entry.save()
