from enum import Enum

KEY_VOLUME = "volume"
KEY_TYPE = "type"


class UserVolumeType(Enum):
    TEST = {KEY_TYPE: "MB", KEY_VOLUME: 1}
    GUEST = {KEY_TYPE: "GB", KEY_VOLUME: 5}
    USER = {KEY_TYPE: "GB", KEY_VOLUME: 20}
    HEAVIER = {KEY_TYPE: "GB", KEY_VOLUME: 100}
