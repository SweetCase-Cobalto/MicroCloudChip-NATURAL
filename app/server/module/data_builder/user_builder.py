from module.data_builder.builder import MicrocloudchipBuilder
from module.label.user_volume_type import UserVolumeType
from django.core.exceptions import ValidationError
from module.MicrocloudchipException.exceptions import MicrocloudchipUserInformationValidateError
from module.validator.user_validator import UserValidator
import app.models as custom_model
import string
import random


class UserBuilder(MicrocloudchipBuilder):
    """
        User 를 생성하기 위한 오구 데이터
        생성하는 클래스
    """

    """
        variable: email:
        variable: name: 사용자 이름
        variable: static_id: 사용자 고유 아이디(자동생성)
        variable: password
        variable: volume_type: 사용자가 사용할 수 있는 최대 용량타입
        variable: is_admin: Admin 여부

        == static functions ==
        function: generate_static_id: user생성 시 랜덤 고유 번호 생성
        
        == set_functions ==
        function: set_email -> this
        function: set_name -> this
        function: set_static_id -> this
        function: set_password -> this
        function: volume_type -> this
        function: set_is_admin -> this
        
        function: build() -> model.User
    """
    email: str = None
    name: str = None
    static_id: str = None
    password: str = None
    volume_type: UserVolumeType = None
    is_admin: bool = None

    """ Validate Functions 
        if failed, call ValidationError
    """

    @staticmethod
    def generate_static_id() -> str:
        # static_id 자동생성
        alphabet = string.ascii_lowercase
        numbers = '0123456789'

        static_id = ""
        
        # 랜덤 생성
        for _ in range(40):
            select = random.randint(0, 1)
            static_id += alphabet[random.randint(0, len(alphabet) - 1)] if select else \
                numbers[random.randint(0, len(numbers) - 1)]
            
        return static_id

    """ set functions 
        계정을 생성하기 위해 데이터들을 세팅하는 set function이다
        builder pattern 이기 때문에 이 밑의 모든 함수들은 자기 자신을 리턴한다.
        
        set functions의 프로세스는 다음과 같다
        1. validate 측정
        2. variable 저장
        3. 자기 자신 리턴
    """
    def set_name(self, new_name: str):
        try:
            UserValidator.validate_name(new_name)
            self.name = new_name
            return self
        except ValidationError as e:
            raise MicrocloudchipUserInformationValidateError(str(e))

    def set_password(self, new_password: str):
        try:
            UserValidator.validate_password(new_password)
            self.password = new_password
            return self
        except ValidationError as e:
            raise MicrocloudchipUserInformationValidateError(str(e))

    def set_volume_type(self, raw_volume_type: str):
        try:
            self.volume_type = UserValidator.validate_volume_type_by_string(raw_volume_type)
            return self
        except ValidationError as e:
            raise MicrocloudchipUserInformationValidateError(str(e))

    def set_email(self, new_email: str):
        try:
            UserValidator.validate_email(new_email)
            self.email = new_email
            return self
        except ValidationError as e:
            raise MicrocloudchipUserInformationValidateError(str(e))

    def set_is_admin(self, new_is_admin: bool):
        try:
            UserValidator.validate_is_admin(new_is_admin)
            self.is_admin = new_is_admin
            return self
        except ValidationError as e:
            raise MicrocloudchipUserInformationValidateError(str(e))

    def set_static_id(self):
        self.static_id = UserBuilder.generate_static_id()
        return self

    # Build To model.User
    def build(self) -> custom_model.User:
        """최종적으로 User Model를 생성한다
            하지만 바로 Database에 저장하지 않는다.
        """
        if not self.name or not self.email or not self.password or \
                self.is_admin is None or not self.static_id or not self.volume_type:
            raise MicrocloudchipUserInformationValidateError("Model User build Error: some data is empty")
        return custom_model.User(
            static_id=self.static_id, name=self.name, pswd=self.password,
            email=self.email, volume_type=self.volume_type.name, is_admin=self.is_admin
        )
