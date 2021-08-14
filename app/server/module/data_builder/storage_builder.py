from abc import ABCMeta, abstractmethod
import os
import sys
from module.data_builder.data_builder import DataBuilder
from module.MicrocloudchipException.exceptions import MicrocloudchipUserDoesNotExistError, \
    MicrocloudchipDirectoryNotFoundError, MicrocloudchipFileAndDirectoryValidateError


class StorageBuilder(DataBuilder):
    """저장소 관련 Builder"""
    """
        system_root: 절대적인 루트를 설정하기 위한 저장소 절대루트
        author_static_id: User static id
        target_root: 운용할 디렉토리 및 파일의 상대적 루트
            target_root 의 절대적 경로: [system_root]/storage/[author]/root/[target_root]
        
    """

    author_static_id: str
    target_root: str
    NAMING_FAILED_CHAR_LIST: list[str] = [':', '*', '?', '''"''', ">", "<", "|"]
    """ 파일 및 디렉토리 이름이 아닌 상대적 루트이므로 \\과 /는 OS에 따라서 선택적으로 판별 """

    """Function
        set_system_root
        set_author_static_id
        set_target_root
        
        @abstractmethod
        get_full_root: 전체 절대경로 출력: 클래스에 따라 같은 static_id, target_root 여도 절대경로가 다를 수 있음
        is_all_have: 해당 요소가 전부다 들어있는 지 확인
        save: 생성(저장)
        delete: 제거
    """

    def set_author_static_id(self, author_static_id: str):
        # 데이터베이스 확인
        import app.models as model
        try:
            model.User.objects.get(static_id=author_static_id)
        except model.User.DoesNotExist:
            raise MicrocloudchipUserDoesNotExistError("User does not exist")

        # 디렉토리 확인
        full_author_root = f"{self.system_root}{self.TOKEN}storage{self.TOKEN}{author_static_id}/root"
        if not os.path.isdir(full_author_root):
            raise MicrocloudchipDirectoryNotFoundError(f"User[{author_static_id}] Directory: Does not exist check "
                                                       f"system storage")
        # 다 있으면 저장
        self.author_static_id = author_static_id

        return self

    def set_target_root(self, target_root):
        # 해당 루트에 금지 문자가 있는 지 확인
        naming_failed_char_list = self.NAMING_FAILED_CHAR_LIST
        if self.TOKEN == '\\':
            naming_failed_char_list += ['/']
        else:
            naming_failed_char_list += ["\\"]

        if any(char in target_root for char in naming_failed_char_list):
            # 금지어 검출
            raise MicrocloudchipFileAndDirectoryValidateError("This root have failed naming character")

        # 디렉토리를 생성할 이전 디렉토리 존재 여부 확인
        # static_id가 선택이 안되었을 경우 에러 호출
        if not self.author_static_id:
            raise ValueError("User Static id is None")

        author_full_root = f"{self.system_root}{self.TOKEN}storage{self.TOKEN}{self.author_static_id}{self.TOKEN}root"
        prev_directory_root = self.TOKEN.join(target_root.split(self.TOKEN)[:-1])
        prev_full_root = author_full_root + self.TOKEN + prev_directory_root

        if not os.path.isdir(prev_full_root):
            # 이전 디렉토리강 없으면 에러 송출
            raise MicrocloudchipDirectoryNotFoundError(f"Prev Directory for add new directory does not exist: "
                                                       f"{prev_full_root}")
        # target root 추가
        self.target_root = target_root
        return self

    @abstractmethod
    def is_all_have(self) -> bool:
        pass

    @abstractmethod
    def get_full_root(self) -> str:
        pass

    @abstractmethod
    def save(self):
        pass
