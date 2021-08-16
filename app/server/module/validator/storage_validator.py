from django.core.exceptions import ValidationError

from module.MicrocloudchipException.exceptions import MicrocloudchipFileAndDirectoryValidateError


class StorageValidator:
    NAMING_FAILED_CHAR_SET: set[str] = {':', '*', '?', '''"''', ">", "<", "|"}
    """ 파일 및 디렉토리 이름이 아닌 상대적 루트이므로 \\과 /는 OS에 따라서 선택적으로 판별 """

    @staticmethod
    def validate_storage(storage_root: str, token: str) -> bool:
        # 해당 루트에 금지 문자가 있는 지 확인
        naming_failed_char_set = StorageValidator.NAMING_FAILED_CHAR_SET
        if token == '\\':
            naming_failed_char_set.add('/')
        else:
            naming_failed_char_set.add('\\')
        if any(char in storage_root for char in naming_failed_char_set):
            return False
        return True

    @staticmethod
    def validate_storage_with_no_django_validator_exception(storage_root: str, token: str):
        if not StorageValidator.validate_storage(storage_root, token):
            raise MicrocloudchipFileAndDirectoryValidateError("This root have failed naming character")

    @staticmethod
    def validate_storage_with_django_validator_exception(storage_root: str, token: str):
        if not StorageValidator.validate_storage(storage_root, token):
            raise ValidationError("This root have failed naming character")