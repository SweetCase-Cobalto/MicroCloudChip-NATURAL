from abc import abstractmethod

from module.data_builder.data_builder import DataBuilder
from module.MicrocloudchipException.exceptions import MicrocloudchipUserDoesNotExistError, \
    MicrocloudchipFileAndDirectoryValidateError


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
    """

    def set_author_static_id(self, author_static_id: str):
        import app.models as model
        try:
            # 데이터베이스에 해당 static id 가 존재하는 지 확인
            model.User.objects.get(static_id=author_static_id)
        except model.User.DoesNotExist:
            raise MicrocloudchipUserDoesNotExistError("User does not exist")

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

        self.target_root = target_root
        return self

    @abstractmethod
    def is_all_have(self) -> bool:
        pass

    def get_full_root(self) -> str:
        # 전체 루트 구하기
        if self.is_all_have():
            return f"{self.system_root}{self.TOKEN}storage" \
                   f"{self.TOKEN}{self.author_static_id}{self.TOKEN}root{self.TOKEN}" \
                   f"{self.target_root}"
        raise ValueError("All data is not filled")

    @abstractmethod
    def save(self):
        pass
