from enum import Enum


class FileType(Enum):
    TEXT = ['txt']
    EXECUTE = ['exe', 'msi']
    PDF = ['pdf']
    AUDIO = ['mp3', 'wav', 'midi', 'mid']
    VIDEO = ['mp4', 'avi']
    IMAGE = ['jpg', 'jpeg', 'png', 'gif']
    OTHER = []

    @staticmethod
    def get_file_type(ex: str):

        if ex in FileType.TEXT.value:
            return FileType.TEXT
        elif ex in FileType.EXECUTE.value:
            return FileType.EXECUTE
        elif ex in FileType.PDF.value:
            return FileType.PDF
        elif ex in FileType.AUDIO.value:
            return FileType.AUDIO
        elif ex in FileType.VIDEO.value:
            return FileType.VIDEO
        elif ex in FileType.IMAGE.value:
            return FileType.IMAGE
        else:
            return FileType.OTHER


class FileVolumeType(Enum):
    BYTE = 10 ** 0
    KB = 10 ** 3
    MB = 10 ** 6
    GB = 10 ** 9
    TB = 10 ** 12

    @staticmethod
    def get_file_volume_type(vol: int, zfill_counter: int = 0) -> tuple:

        _vol = -1

        if vol < FileVolumeType.KB.value:
            vol_type, _vol = FileVolumeType.BYTE, vol
        elif vol < FileVolumeType.MB.value:
            vol_type, _vol = FileVolumeType.KB, vol / FileVolumeType.KB.value
        elif vol < FileVolumeType.GB.value:
            vol_type, _vol = FileVolumeType.MB, vol / FileVolumeType.MB.value
        elif vol < FileVolumeType.TB.value:
            vol_type, _vol = FileVolumeType.GB, vol / FileVolumeType.GB.value
        else:
            vol_type, _vol = FileVolumeType.TB, vol / FileVolumeType.TB.value

        return vol_type, (_vol if zfill_counter < 1 else round(_vol, zfill_counter))

    @staticmethod
    def type_to_num(vol_type, vol: int) -> int:
        # 바이트 전환
        r = vol * vol_type.value
        return r

    @staticmethod
    def add(num1: tuple, num2: tuple, zfill_counter: int = 0) -> tuple:
        """
            param:
                tuple:
                    (int, VolumeType)
        """
        # 바이트 단위로 전환
        n1 = FileVolumeType.type_to_num(num1[0], num1[1])
        n2 = FileVolumeType.type_to_num(num2[0], num2[1])
        n = n1 + n2
        return FileVolumeType.get_file_volume_type(n, zfill_counter)

    @staticmethod
    def sub(num1: tuple, num2: tuple, zfill_counter: int = 0) -> tuple:
        n1 = FileVolumeType.type_to_num(num1[0], num1[1])
        n2 = FileVolumeType.type_to_num(num2[0], num2[1])
        n = n1 - n2
        return FileVolumeType.get_file_volume_type(n, zfill_counter)

    @staticmethod
    def cut_zfill(r: tuple, zfill_counter: int):
        v_type, val = r
        raw_val = FileVolumeType.type_to_num(v_type, val)
        return FileVolumeType.get_file_volume_type(raw_val, zfill_counter)
