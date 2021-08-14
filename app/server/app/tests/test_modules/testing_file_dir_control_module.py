from module.data_builder.directory_builder import DirectoryBuilder


def test_make_directory(req):
    directory_builder = DirectoryBuilder()
    directory_builder.set_system_root(req['system-root']) \
        .set_author_static_id(req['static-id']) \
        .set_target_root(req['target-root']).save()
