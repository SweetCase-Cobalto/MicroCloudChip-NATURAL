from module.MicrocloudchipException.exceptions import MicrocloudchipFileAlreadyExistError, \
    MicrocloudchipDirectoryNotFoundError, MicrocloudchipDirectoryAlreadyExistError
from module.data_builder.storage_builder import StorageBuilder
import os


class FileBuilder(StorageBuilder):
    raw_data: bytes

    def set_raw_data(self, raw_data: bytes):
        self.raw_data = raw_data
        return self

    def is_all_have(self) -> bool:
        if not self.raw_data or not self.TOKEN or \
                not self.author_static_id or not self.target_root or \
                not self.system_root:
            return False
        return True

    def save(self):
        try:
            full_root = self.get_full_root()
        except ValueError as e:
            raise e
        # 이미 파일 및 디렉토리가 존재하는 경우
        if os.path.isfile(full_root):
            raise MicrocloudchipFileAlreadyExistError(f"File {self.target_root} is already exist")
        elif os.path.isdir(full_root):
            raise MicrocloudchipDirectoryAlreadyExistError(f"Directory {self.target_root} is aleady exist")

        # 생성을 해야 하는 데
        # 파일을 저장 할 디렉토리가 존재하는 지 찾아봐야 한다.
        else:
            slash_idx = -1
            for i in range(len(full_root) - 1, -1, -1):
                if full_root[i] == self.TOKEN:
                    slash_idx = i
                    break
            if not os.path.isdir(full_root[:slash_idx]):
                raise MicrocloudchipDirectoryNotFoundError(f"Prev Directory for add new directory does not exist")

            # 파일 저장
            with open(full_root, 'wb') as f:
                f.write(self.raw_data)
