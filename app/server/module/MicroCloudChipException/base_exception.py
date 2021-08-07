class MicroCloudChipException(Exception):
    def __init__(self, err_msg: str):
        super().__init__(err_msg)