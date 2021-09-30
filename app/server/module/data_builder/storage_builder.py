import os
from abc import abstractmethod

from module.data_builder.data_builder import DataBuilder
from module.MicrocloudchipException.exceptions import MicrocloudchipUserDoesNotExistError
from module.validator.storage_validator import StorageValidator


class StorageBuilder(DataBuilder):
    """저장소 관련 Builder
        파일 및 디렉토리를 생성할 때 사용되는 클래스다
    """
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

    def set_author_static_id(self, author_static_id: str):
        import app.models as model
        try:
            # 데이터베이스에 해당 static id 가 존재하는 지 확인
            model.User.objects.get(static_id=author_static_id)
        except model.User.DoesNotExist:
            raise MicrocloudchipUserDoesNotExistError("User does not exist")
        
        # static_id 저장
        self.author_static_id = author_static_id

        return self

    def set_target_root(self, target_root):
        # 해당 루트에 금지 문자가 있는 지 확인
        StorageValidator.validate_storage_with_no_django_validator_exception(target_root)
        # target_root 변경
        self.target_root = os.path.join(*(target_root.split('/')))
        return self

    @abstractmethod
    def is_all_have(self) -> bool:
        # 모든 변수가 존재하는 경우
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
