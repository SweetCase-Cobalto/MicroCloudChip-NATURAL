from module.data_builder.directory_builder import DirectoryBuilder
from module.data_builder.file_builder import FileBuilder


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
