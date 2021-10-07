from abc import abstractmethod
from typing import Dict, Optional

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

    @abstractmethod
    def __call__(self):
        pass


class SharedFileData(SharedStorageData):

    def __init__(self, static_id: str, target_root: str):
        self.target_root = target_root
        self.static_id = static_id
        self.is_called = False

    def __call__(self):
        try:
            sf: model.SharedFile = model.SharedFile.objects \
                .filter(user_static_id=self.static_id) \
                .get(file_root=self.target_root)

            serial = SharedFileSerializer(sf)
            raw_data: Dict[Optional] = serial.data
            raw_data['start_date'] = serial.change_start_date_to_datetime(raw_data['start_date'])

            self.start_date = raw_data['start_date']
            self.shared_id = raw_data['shared_id']

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
