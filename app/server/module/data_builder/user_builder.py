from module.label.user_volume_type import UserVolumeType
from django.core.exceptions import ValidationError
from module.MicrocloudchipException.exceptions import MicrocloudchipUserInformationValidateError
from module.validator.user_validator import UserValidator
import app.models as custom_model
import string
import random


class UserBuilder:
    """
        User 를 생성하기 위한 오구 데이터
        생성하는 클래스
    """

    """
        variable: email:
        variable: name: 사용자 이름
        variable: static_id: 사용자 고유 아이디(자동생성)
        variable: password
        variable: volume_type
        variable: is_admin

        == private functions ==
        function: generate_static_id
        
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

        for _ in range(40):
            select = random.randint(0, 1)
            if select:
                # alphabet
                static_id += alphabet[random.randint(0, len(alphabet) - 1)]
            else:
                # number
                static_id += numbers[random.randint(0, len(numbers) - 1)]

        return static_id

    """ set functions """

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
        if not self.name or not self.email or not self.password or \
                self.is_admin is None or not self.static_id or not self.volume_type:
            raise MicrocloudchipUserInformationValidateError("Model User build Error: some data is empty")
        return custom_model.User(
            static_id=self.static_id, name=self.name, pswd=self.password,
            email=self.email, volume_type=self.volume_type.name, is_admin=self.is_admin
        )
