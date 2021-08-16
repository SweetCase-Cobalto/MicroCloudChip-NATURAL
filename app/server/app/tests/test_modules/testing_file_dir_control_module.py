from module.data_builder.directory_builder import DirectoryBuilder
from module.data_builder.file_builder import FileBuilder
from module.data.storage_data import *
import os


def test_make_directory(req):
    directory_builder = DirectoryBuilder()
    directory_builder.set_system_root(req['system-root']) \
        .set_author_static_id(req['static-id']) \
        .set_target_root(req['target-root']).save()


def test_upload_file_routine(req) -> bool:
    file_builder = FileBuilder()
    file_builder.set_system_root(req['system-root']) \
        .set_author_static_id(req['static-id']) \
        .set_target_root(req['target-root']) \
        .set_raw_data(req['raw-data']).save()

    # 업로드 성공 여부
    return os.path.isfile(file_builder.get_full_root())


def test_get_file_information(req) -> FileData:
    static_id = req['static-id']
    target_root = req['target-root']
    system_root = req['system-root']
    root_token = req['root-token']

    full_root = f"{system_root}{root_token}storage{root_token}{static_id}{root_token}root{root_token}{target_root}"
    f = FileData(full_root)()
    return f


def test_remove_file_routine(f_information: FileData):
    full_root = f_information['full-root']
    f_information.remove()
    return not os.path.isfile(full_root)


def test_get_directory_info_routine(req):
    static_id = req['static-id']
    target_root = req['target-root']
    system_root = req['system-root']
    root_token = req['root-token']

    full_root = f"{system_root}{root_token}storage{root_token}{static_id}{root_token}root"
    if target_root and len(target_root) > 0:
        full_root += f"{root_token}{target_root}"

    d = DirectoryData(full_root)()

    return d
