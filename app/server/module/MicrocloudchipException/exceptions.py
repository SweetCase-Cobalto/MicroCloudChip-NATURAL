from module.MicrocloudchipException.base_exception import MicrocloudchipException

# Prefixes
SYSTEM_PREFIX = 0x00000000
USER_PREFIX = 0x01000000
STORAGE_PREFIX = 0x02000000
ACCESS_PREFIX = 0x03000000


class MicrocloudchipSucceed(MicrocloudchipException):
    # 정상 접근 (보통 API 가 제대로 응답 했을 경우 이 코드를 전송한다.)
    def __init__(self):
        super().__init__("Success", 0x00)


class MicrocloudchipSystemConfigFileNotFoundError(MicrocloudchipException):
    # config file 못찾음
    def __init__(self):
        super().__init__("System Config File Not Found", 0x00000001 | SYSTEM_PREFIX)


class MicrocloudchipSystemConfigFileParsingError(MicrocloudchipException):
    # config.json 파싱 에러
    def __init__(self, err_msg: str):
        super().__init__(err_msg, 0x00000002 | SYSTEM_PREFIX)


class MicrocloudchipSystemAbnormalAccessError(MicrocloudchipException):
    # 비정상 접근 에러
    def __init__(self, err_msg: str):
        super().__init__(err_msg, 0x03 | SYSTEM_PREFIX)


class MicrocloudchipLoginConnectionExpireError(MicrocloudchipException):
    # 로그인 만료
    def __init__(self, err_msg: str):
        super().__init__(err_msg, 0x04 | SYSTEM_PREFIX)


# Add In 0.1.0
class MicrocloudchipSystemInternalException(MicrocloudchipException):
    # Microcloudchip관련 에러가 아닌 내부 에러가 발생한 경우
    # msg는 직접 세팅한다.
    def __init__(self, __e: Exception):
        err_msg: str = f"Internal Exception Occured: {type(__e).__name__}:{__e}"
        super().__init__(err_msg, 0x05 | SYSTEM_PREFIX)


# User Exception
class MicrocloudchipUserInformationValidateError(MicrocloudchipException):
    def __init__(self, err_msg: str):
        super().__init__(err_msg, 0x00000001 | USER_PREFIX)


class MicrocloudchipUserUploadFailedError(MicrocloudchipException):
    def __init__(self, err_msg: str):
        super().__init__(err_msg, 0x00000002 | USER_PREFIX)


class MicrocloudchipUserDoesNotExistError(MicrocloudchipException):
    def __init__(self, err_msg: str):
        super().__init__(err_msg, 0x00000003 | USER_PREFIX)


class MicrocloudchipLoginFailedError(MicrocloudchipException):
    def __init__(self, err_msg: str):
        super().__init__(err_msg, 0x04 | USER_PREFIX)


# File/Data Exception
class MicrocloudchipDirectoryNotFoundError(MicrocloudchipException):
    def __init__(self, err_msg: str):
        super().__init__(err_msg, 0x00000001 | STORAGE_PREFIX)


class MicrocloudchipFileNotFoundError(MicrocloudchipException):
    def __init__(self, err_msg: str):
        super().__init__(err_msg, 0x00000002 | STORAGE_PREFIX)


class MicrocloudchipFileAndDirectoryValidateError(MicrocloudchipException):
    def __init__(self, err_msg: str):
        super().__init__(err_msg, 0x00000003 | STORAGE_PREFIX)


class MicrocloudchipDirectoryAlreadyExistError(MicrocloudchipException):
    def __init__(self, err_msg: str):
        super().__init__(err_msg, 0x00000004 | STORAGE_PREFIX)


class MicrocloudchipFileAlreadyExistError(MicrocloudchipException):
    def __init__(self, err_msg: str):
        super().__init__(err_msg, 0x00000005 | STORAGE_PREFIX)


class MicrocloudchipStorageOverCapacityError(MicrocloudchipException):
    def __init__(self, err_msg: str):
        super().__init__(err_msg, 0x06 | STORAGE_PREFIX)


class MicrocloudchipDirectoryDeleteFailedBacauseOfSomeData(MicrocloudchipException):
    def __init__(self, err_msg: str):
        super().__init__(err_msg, 0x07 | STORAGE_PREFIX)


# Add in 0.0.4
class MicrocloudchipFileAndDirectoryNameEmpty(MicrocloudchipException):
    def __init__(self, err_msg: str):
        super().__init__(err_msg, 0x08 | STORAGE_PREFIX)


# Add In 0.1.0
class MicrocloudchipSharedFileAlreadyExistError(MicrocloudchipException):
    def __init__(self, err_msg: str):
        super().__init__(err_msg, 0x09 | STORAGE_PREFIX)


class MicrocloudchipFileIsNotSharedError(MicrocloudchipException):
    def __init__(self, err_msg: str):
        super().__init__(err_msg, 0x0A | STORAGE_PREFIX)


class MicrocloudchipFileSharedButRemovedError(MicrocloudchipException):
    def __init__(self, err_msg: str):
        super().__init__(err_msg, 0x0B | STORAGE_PREFIX)


class MicrocloudchipDataFormatNotCalled(MicrocloudchipException):
    def __init__(self, err_msg: str):
        super().__init__(err_msg, 0x0C | STORAGE_PREFIX)


# AccessException
class MicrocloudchipAuthAccessError(MicrocloudchipException):
    def __init__(self, err_msg: str):
        super().__init__(err_msg, 0x1 | ACCESS_PREFIX)
