import os
from abc import abstractmethod
from typing import Dict, Optional, List

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
            real_root: str = os.path.join(self.system_root, "storage", self.static_id, "root", self.target_root)
            if not os.path.isfile(real_root):
                # Unshare 처리
                self.is_called = True
                self.unshare()
                raise MicrocloudchipFileNotFoundError("File Is Not Exist")

            self.is_called = True
            return self

        except Exception as e:
            raise MicrocloudchipFileIsNotSharedError("This File is not shared")

    def unshare(self):
        if not self.is_called:
            raise MicrocloudchipDataFormatNotCalled("Data is not called yet")
        else:
            data = SharedFileSerializer(data={"start_date": self.start_date,
                                              "user_static_id": self.static_id,
                                              "file_root": self.target_root,
                                              "shared_id": self.shared_id})

            data.build().delete()

    def __str__(self):
        # Real Root 출력
        return os.path.join(self.system_root, "storage", self.static_id, "root", self.target_root)

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

