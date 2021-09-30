from enum import Enum, unique

from module.label.file_type import FileVolumeType


@unique
class UserVolumeTypeKeys(Enum):
    KEY_VOLUME = "volume"
    KEY_TYPE = "type"


@unique
class UserVolumeType(Enum):
    TEST = {UserVolumeTypeKeys.KEY_TYPE: FileVolumeType.KB, UserVolumeTypeKeys.KEY_VOLUME: 1}
    GUEST = {UserVolumeTypeKeys.KEY_TYPE: FileVolumeType.GB, UserVolumeTypeKeys.KEY_VOLUME: 5}
    USER = {UserVolumeTypeKeys.KEY_TYPE: FileVolumeType.GB, UserVolumeTypeKeys.KEY_VOLUME: 20}
    HEAVIER = {UserVolumeTypeKeys.KEY_TYPE: FileVolumeType.GB, UserVolumeTypeKeys.KEY_VOLUME: 100}

    def __int__(self):
        # 실제 가용 용랑 단위 계싼
        return FileVolumeType.type_to_num(
            self.value[UserVolumeTypeKeys.KEY_TYPE],
            self.value[UserVolumeTypeKeys.KEY_VOLUME]
        )

    def to_tuple(self):
        return self.value[UserVolumeTypeKeys.KEY_TYPE], self.value[UserVolumeTypeKeys.KEY_VOLUME]
