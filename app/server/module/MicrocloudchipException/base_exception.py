class MicrocloudchipException(Exception):
    errorCode: int

    def __init__(self, err_msg: str, errorCode: int):
        super().__init__(err_msg)
        self.errorCode = errorCode
