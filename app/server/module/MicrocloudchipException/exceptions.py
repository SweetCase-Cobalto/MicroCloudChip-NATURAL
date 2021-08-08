from module.MicrocloudchipException.base_exception import MicrocloudchipException


class MicrocloudchipSystemConfigFileNotFoundError(MicrocloudchipException):
    # config file 못찾음
    def __init__(self):
        super().__init__("System Config File Not Found")


class MicrocloudchipSystemConfigFileParsingError(MicrocloudchipException):
    # config.json 파싱 에러
    def __init__(self, err_msg: str):
        super().__init__(err_msg)