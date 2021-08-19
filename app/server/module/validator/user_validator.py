from django.core.exceptions import ValidationError

from module.label.user_volume_type import UserVolumeType
import re


class UserValidator:

    @staticmethod
    def validate_email(email: str):

        if not isinstance(email, str):
            raise ValidationError("email match error: email must be string")

        p = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$')

        if not p.match(email):
            raise ValidationError("email match error: email is not valid")

    @staticmethod
    def validate_name(name: str):

        if not isinstance(name, str):
            raise ValidationError("name match error: name must be string")

        p = re.compile('^[a-zA-Z0-9]{4,16}$')

        if not p.match(name):
            raise ValidationError("name match error: name is not valid")

    @staticmethod
    def validate_static_id(static_id: str):

        if not isinstance(static_id, str):
            raise ValidationError("static_id match error: name must be string")

        p = re.compile('^[a-z0-9]{40}$')

        if p.match(static_id):
            raise ValidationError("static_id match error: static_id is not valid")

    @staticmethod
    def validate_password(password: str):

        if not isinstance(password, str):
            raise ValidationError("password match error: password must be string")

        if not 8 <= len(password) <= 128:
            raise ValidationError("password match error: password is not valid")

    @staticmethod
    def validate_volume_type_by_string(type_string: str) -> UserVolumeType:

        if not isinstance(type_string, str):
            raise ValidationError("volume type match error: volume type must be string")

        for volume_type in UserVolumeType:
            if type_string == volume_type.name:
                return volume_type

        # Not Found
        raise ValidationError("volume type match error; volume type is not valid")

    @staticmethod
    def validate_is_admin(new_is_admin: bool):
        if not isinstance(new_is_admin, bool):
            raise ValidationError("is_admin match error: is_admin must be boolean")