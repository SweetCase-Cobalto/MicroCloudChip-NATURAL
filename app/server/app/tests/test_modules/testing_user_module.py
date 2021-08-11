from module.data_builder.user_builder import UserBuilder
import app.models as model
from module.MicrocloudchipException.exceptions import MicrocloudchipUserUploadFailedError, \
    MicrocloudchipUserInformationValidateError
import os
import sys
import shutil


def test_set_info_to_user_builder(user_builder: UserBuilder, req: dict):
    try:
        user_builder.set_name(req['name']) \
            .set_password(req['pswd']) \
            .set_email(req['email']) \
            .set_volume_type(req['volume-type']) \
            .set_is_admin(req['is-admin']) \
            .set_static_id()
    except KeyError as e:
        raise MicrocloudchipUserInformationValidateError(str(e))


def test_upload_user_in_step_routinetest(model_user: model.User, system_root: str, user_img_example_root: str = None):
    while True:
        # 중복되는 static_id가 있는 지 확인
        try:
            model.User.objects.get(static_id=model_user.static_id)
        except model.User.DoesNotExist:
            # 일치하는 static id 없음
            break

        # 존재함
        model_user.static_id = UserBuilder.generate_static_id()

    # Email 중복 확인
    try:
        model.User.objects.get(email=model_user.email)
    except model.User.DoesNotExist:

        # 데이터 업로드
        model_user.save()


        # 유저 스토리지 생성
        # OS에 따라 디렉토리 토큰이 달라진다
        dir_token = '\\' if sys.platform == "win32" else '/'

        # 생성
        user_root = f"{system_root}{dir_token}storage{dir_token}{model_user.static_id}"
        os.mkdir(user_root)
        os.mkdir(user_root + dir_token + "root")  # 디렉토리 및 파일이 저장될 장소
        os.mkdir(user_root + dir_token + "asset")  # 설정파일이 저장 될 장소

        # 이미지파일 생성
        if user_img_example_root:
            with open(user_img_example_root, 'rb') as src:
                ex = user_img_example_root.split('.')[-1]
                with open(user_root + dir_token + 'asset' + dir_token + "user." + ex, 'wb') as dst:
                    dst.writelines(src.readlines())
        return

    raise MicrocloudchipUserUploadFailedError("same email user is exist")


def test_reset_because_of_failed_upload_failed(static_id_list: list[str], system_root: str):
    # 테스트 실패할 경우 Reset
    for static_id in static_id_list:
        try:
            instance = model.User.objects.get(static_id=static_id)
            instance.delete()
        except model.User.DoesNotExist:
            print("not_exist")
            continue

    # 전부 삭제
    dir_token = '\\' if sys.platform == "win32" else '/'
    storage_root = f"{system_root}{dir_token}storage"

    shutil.rmtree(storage_root)
    os.mkdir(storage_root)