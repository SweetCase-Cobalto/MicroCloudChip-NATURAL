from abc import ABCMeta, abstractmethod
from datetime import datetime
import os, sys, shutil

from module.MicrocloudchipException.exceptions import MicrocloudchipFileNotFoundError, \
    MicrocloudchipFileAlreadyExistError, MicrocloudchipDirectoryNotFoundError, MicrocloudchipDirectoryAlreadyExistError
from module.label.file_type import FileType, FileVolumeType


class StorageData(metaclass=ABCMeta):
    # 파일 및 디렉토리를 검색할 때 결과를 출력하기 위한 객체
    # call 함수를 사용해서 데이터를 불러온다.
    name: str
    modify_date: datetime
    create_date: datetime
    raw_volume: int
    full_root: str
    is_called: bool = False
    token: str = '\\' if sys.platform == 'win32' else '/'

    def __init__(self, full_root: str):
        # 데이터를 가져올 대상 루트를 저장
        self.full_root = full_root

    @abstractmethod
    def __call__(self):
        # 로컬 저장소로부터 데이터를 갖고와서 변수에 저장하기
        # 그렇기 때문에 full root 가 없으면 실행이 불가하다
        if not self.full_root:
            raise ValueError("Root is not selected")

    @abstractmethod
    def __getitem__(self, item: str):
        # 데이터 요소를 불러오는 데 사용한다.
        # 그러나 데이터를 미리 불러오지 않았을 경우 데이터가 없으므로 에러가 발생한다
        if not self.is_called:
            raise ValueError("You must get storage data by using __call__()")

    @abstractmethod
    def __str__(self) -> str:
        # 데이터 요약 본 출력
        # 테스트 할 때 만 쓰세요
        pass

    @abstractmethod
    def remove(self):
        # 파일이나 디렉토리를 삭제
        if not self.is_called:
            raise ValueError("You must get storage data by using __call__()")


class FileData(StorageData):
    file_type: FileType
    volume: int
    volume_unit: FileVolumeType

    def __init__(self, full_root: str):
        super().__init__(full_root)

    def __call__(self):
        super().__call__()

        # 파일 여부 확인
        if not os.path.isfile(self.full_root):
            raise MicrocloudchipFileNotFoundError(f"file: {self.full_root} does not exist")

        # 있으면 데이터 갖고오기
        file_stat = os.stat(self.full_root)
        self.create_date = datetime.fromtimestamp(file_stat.st_ctime)
        self.modify_date = datetime.fromtimestamp(file_stat.st_mtime)
        self.name = self.full_root.split(self.token)[-1]
        self.file_type = FileType.get_file_type(self.name.split('.')[-1])

        # 데이터 크기 갖고오기
        _volume = file_stat.st_size
        self.raw_volume = _volume
        self.volume_unit, self.volume = FileVolumeType.get_file_volume_type(_volume, 2)

        self.is_called = True

        return self

    def __getitem__(self, item: str):
        super().__getitem__(item)

        if item == 'create-date':
            return self.create_date
        elif item == 'modify-date':
            return self.modify_date
        elif item == 'file-name':
            return self.name
        elif item == 'file-type':
            return self.file_type
        elif item == 'size':
            return self.volume_unit, self.volume
        elif item == 'size-raw':
            return self.raw_volume
        elif item == 'full-root':
            return self.full_root
        else:
            raise KeyError(f"file data key error: {item}")

    def __str__(self):
        r = ""
        if not self.is_called:
            r = f"This Class is not called yet, root: {self.full_root}"
        else:
            r += f"filename: {self.name}\n"
            r += f"filetype: {self.file_type.name}\n"
            r += f"create date: {self.create_date}\n"
            r += f"modify date: {self.modify_date}\n"
            r += f"size: {self.volume} {self.volume_unit.name}\n"
            r += f"full root: {self.full_root}\n"
        return r

    def remove(self):
        super().remove()
        self.__call__()
        if os.path.isfile(self.full_root):
            os.remove(self.full_root)
        self.is_called = False

    def update_name(self, new_name: str):
        # 업데이트 시도
        # 파일 이름이 다를 경우 MicrocloudchipFileNotFoundError
        self.__call__()

        # 파일 이름 변경
        if new_name == self.name:
            # 이름이 같은건 생성 불가
            raise ValueError("same filename")

        # 파일 이름 변경
        new_full_root = self.token.join(self.full_root.split(self.token)[:-1] + [new_name])

        try:
            os.rename(self.full_root, new_full_root)
        except FileExistsError:
            raise MicrocloudchipFileAlreadyExistError("File that new named is already exist")

        # 이름 바구기에 성공했을 경우 속성 변경
        self.full_root = new_full_root
        self.name = new_name
        self.__call__()


class DirectoryData(StorageData):
    file_list: list[dict]

    def __init__(self, full_root: str):
        super().__init__(full_root)

    def __call__(self):
        super().__call__()

        # 디렉토리 여부 확인
        if not os.path.isdir(self.full_root):
            raise MicrocloudchipDirectoryNotFoundError(f"Directory {self.full_root} not found")

        # 데이터 갖고오기
        file_stat = os.stat(self.full_root)
        self.create_date = datetime.fromtimestamp(file_stat.st_ctime)
        self.modify_date = datetime.fromtimestamp(file_stat.st_mtime)
        self.name = self.full_root.split(self.token)[-1]

        file_list = os.listdir(self.full_root)
        self.file_list = []
        # 디렉토리 파일을 구별해야 한다
        for f in file_list:
            d = {"name": f}
            if os.path.isfile(self.full_root + self.token + f):
                d['type'] = 'file'
            else:
                d['type'] = 'directory'
            self.file_list.append(d)
        self.is_called = True
        return self

    def __getitem__(self, item: str):
        super().__getitem__(item)

        if item == 'create-date':
            return self.create_date
        elif item == 'modify-date':
            return self.modify_date
        elif item == 'dir-name':
            return self.name
        elif item == 'file-list':
            return self.file_list
        elif item == 'file-size':
            return len(self.file_list)
        elif item == 'full-root':
            return self.full_root
        else:
            raise KeyError(f"file data key error: {item}")

    def __str__(self):
        r = ""
        if not self.is_called:
            r = f"This Class is not called yet, root: {self.full_root}"
        else:
            r += f"dir name: {self.name}\n"
            r += f"create date: {self.create_date}\n"
            r += f"modify date: {self.modify_date}\n"
            r += f"files: {self['file-list']}\n"
            r += f"full root: {self.full_root}\n"
        return r

    def update_name(self, new_name: str):
        # 디렉토리 이름 변경
        # TODO: Warning: 루트 디렉토리 변경을 막는 부분은 Manager 단계에서 진행하므로 여기서는 예외처리를 하지 않는다.

        self.__call__()  # 업데이트 시도
        # 실패 시 Directory Not Found

        if new_name == self.name:
            raise ValueError("same directory name")

        # 파일 이름 변경
        new_full_root = self.token.join(self.full_root.split(self.token)[:-1] + [new_name])
        try:
            os.rename(self.full_root, new_full_root)
        except FileExistsError:
            raise MicrocloudchipDirectoryAlreadyExistError("Directory that new named is aleady exist")

        # 이름 바꾸기에 성공했을 경우 속성 변경
        self.full_root = new_full_root
        self.name = new_name
        self.__call__()  # 다시 업데이트

    def remove(self):
        super().remove()
        self.__call__()
        if os.path.isdir(self.full_root):
            shutil.rmtree(self.full_root)
        self.is_called = False