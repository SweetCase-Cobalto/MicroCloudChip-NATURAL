from enum import Enum, unique


@unique
class FileType(Enum):
    # 아래 확장자에[ 따라 설정되는 파일 타입이 달라진다
    TEXT = ['txt']
    EXECUTE = ['exe', 'msi']
    PDF = ['pdf']
    AUDIO = ['mp3', 'wav', 'midi', 'mid']
    VIDEO = ['mp4', 'avi']
    IMAGE = ['jpg', 'jpeg', 'png', 'gif']
    OTHER = []

    @staticmethod
    def get_file_type(ex: str):
        # File Type 갖고오기

        for f_type in FileType:
            if ex in f_type.value:
                return f_type
        return FileType.OTHER


@unique
class FileVolumeType(Enum):
    # Volume 단위임

    BYTE = 10 ** 0
    KB = 10 ** 3
    MB = 10 ** 6
    GB = 10 ** 9
    TB = 10 ** 12

    @staticmethod
    def get_file_volume_type(vol: int, zfill_counter: int = 0) -> tuple:
        # raw data size에서 맞는 단위 구하기
        
        # Enum 요소들을 list로 표현
        e_list = list(FileVolumeType.__dict__['_member_map_'].values())
        vol_type, _vol = e_list[-1], vol / e_list[-1].value
        for i in range(1, len(e_list)):
            if vol < e_list[i].value:
                vol_type, _vol = e_list[i-1], vol / e_list[i-1].value
                break
        return vol_type, (_vol if zfill_counter < 1 else round(_vol, zfill_counter))

    @staticmethod
    def type_to_num(vol_type, vol: int) -> int:
        # 바이트 전환
        # 1KB는 1000 이 리턴된다.
        r = vol * vol_type.value
        return r

    @staticmethod
    def add(num1: tuple, num2: tuple, zfill_counter: int = 0) -> tuple:
        # (int, volumetype) 간의 덧셈 연산
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
        # (int, volumetype) 간의 뺄셈 연산
        n1 = FileVolumeType.type_to_num(num1[0], num1[1])
        n2 = FileVolumeType.type_to_num(num2[0], num2[1])
        n = n1 - n2
        return FileVolumeType.get_file_volume_type(n, zfill_counter)

    @staticmethod
    def cut_zfill(r: tuple, zfill_counter: int):
        v_type, val = r
        raw_val = FileVolumeType.type_to_num(v_type, val)
        return FileVolumeType.get_file_volume_type(raw_val, zfill_counter)
