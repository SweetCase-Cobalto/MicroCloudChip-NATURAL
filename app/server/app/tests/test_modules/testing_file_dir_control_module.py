from module.data_builder.directory_builder import DirectoryBuilder
from module.data_builder.file_builder import FileBuilder
import os

def test_make_directory(req):
    directory_builder = DirectoryBuilder()
    directory_builder.set_system_root(req['system-root']) \
        .set_author_static_id(req['static-id']) \
        .set_target_root(req['target-root']).save()


def test_upload_file(req):
    file_builder = FileBuilder()
    file_builder.set_system_root(req['system-root']) \
        .set_author_static_id(req['static-id']) \
        .set_target_root(req['target-root']) \
        .set_raw_data(req['raw-data']).save()
    
    # 업로드 성공 여부
    return os.path.isfile(file_builder.get_full_root())
