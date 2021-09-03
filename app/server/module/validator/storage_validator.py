from django.core.exceptions import ValidationError

from module.MicrocloudchipException.exceptions import MicrocloudchipFileAndDirectoryValidateError


class StorageValidator:
    NAMING_FAILED_CHAR_SET: set[str] = {':', '*', '?', '''"''', ">", "<", "|", "\\"}

    @staticmethod
    def validate_storage(storage_root: str) -> bool:
        # 해당 루트에 금지 문자가 있는 지 확인
        naming_failed_char_set = StorageValidator.NAMING_FAILED_CHAR_SET
        if any(char in storage_root for char in naming_failed_char_set):
            return False
        
        # 점 한/두개 짜리 이름의 파일은 만들 수 없음
        final_root: str = storage_root.split('/')[-1]
        if final_root == "." or final_root == "..":
            return False
        return True

    @staticmethod
    def validate_storage_with_no_django_validator_exception(storage_root: str):
        if not StorageValidator.validate_storage(storage_root):
            raise MicrocloudchipFileAndDirectoryValidateError("This root have failed naming character")

    @staticmethod
    def validate_storage_with_django_validator_exception(storage_root: str):
        if not StorageValidator.validate_storage(storage_root):
            raise ValidationError("This root have failed naming character")
