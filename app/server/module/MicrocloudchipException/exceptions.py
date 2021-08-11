from module.MicrocloudchipException.base_exception import MicrocloudchipException

# Prefixes
SYSTEM_PREFIX = 0x00000000
USER_PREFIX = 0x01000000


class MicrocloudchipSystemConfigFileNotFoundError(MicrocloudchipException):
    # config file 못찾음
    def __init__(self):
        super().__init__("System Config File Not Found", 0x00000001 | SYSTEM_PREFIX)


class MicrocloudchipSystemConfigFileParsingError(MicrocloudchipException):
    # config.json 파싱 에러
    def __init__(self, err_msg: str):
        super().__init__(err_msg, 0x00000002 | SYSTEM_PREFIX)


# User Exception
class MicrocloudchipUserInformationValidateError(MicrocloudchipException):
    def __init__(self, err_msg: str):
        super().__init__(err_msg, 0x00000001 | USER_PREFIX)


class MicrocloudchipUserUploadFailedError(MicrocloudchipException):
    def __init__(self, err_msg: str):
        super().__init__(err_msg, 0x00000002 | USER_PREFIX)