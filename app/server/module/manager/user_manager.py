import os
import shutil

import app.models as model
from module.MicrocloudchipException.exceptions import MicrocloudchipAuthAccessError, MicrocloudchipLoginFailedError
from module.data_builder.user_builder import UserBuilder
from module.label.user_volume_type import UserVolumeType, UserVolumeTypeKeys
from module.manager.storage_manager import StorageManager
from module.manager.worker_manager import WorkerManager
from module.specification.System_config import SystemConfig
from module.validator.user_validator import UserValidator
from module.label.file_type import FileVolumeType


class UserManager(WorkerManager):
    AVAILABLE_IMG_EXTENSIONS: list[str] = ['jpg', 'png']

    def __new__(cls, config: SystemConfig):
        if not hasattr(cls, 'user_manager_instance'):
            cls.instance = super(WorkerManager, cls).__new__(cls)
        return cls.instance

    def __make_user_directory(self, user_static_id: str) -> list[str]:
        # User Directory 생성
        # 절대 Class 외에 사용하지 말 것
        super_dir_root = [self.config.get_system_root(), 'storage', user_static_id]
        storage_root = super_dir_root + ['root']
        asset_root = super_dir_root + ['asset']

        if os.path.isdir(os.path.join(*super_dir_root)):
            shutil.rmtree(os.path.join(*super_dir_root))
        if os.path.isdir(os.path.join(*storage_root)):
            shutil.rmtree(os.path.join(*storage_root))
        if os.path.isdir(os.path.join(*asset_root)):
            shutil.rmtree(os.path.join(*asset_root))

        os.mkdir(os.path.join(*super_dir_root))
        os.mkdir(os.path.join(*storage_root))
        os.mkdir(os.path.join(*asset_root))

        return super_dir_root

    def __init__(self, system_config: SystemConfig):
        super().__init__(system_config)

        admin_num: int = len(model.User.objects.filter(is_admin=True))

        if admin_num == 0:
            # 없다면 system_config 에 존재하는 데이터를 바탕으로  어드민을 생성한다.

            admin_email = self.config.get_admin_eamil()
            new_admin_builder: UserBuilder = UserBuilder().set_name('admin') \
                .set_password('12345678') \
                .set_email(admin_email) \
                .set_volume_type('GUEST') \
                .set_is_admin(True) \
                .set_static_id()

            while True:
                try:
                    model.User.objects.get(static_id=new_admin_builder.static_id)
                except model.User.DoesNotExist:
                    break
                new_admin_builder.set_static_id()

            # Directory 생성
            admin_static_id = new_admin_builder.static_id
            self.__make_user_directory(admin_static_id)

            # DB 저장
            new_admin_builder.build().save()

    def login(self, user_email: str, user_password: str) -> dict:

        r = model.User.objects.filter(email=user_email).filter(pswd=user_password)
        if len(r) == 0:
            raise MicrocloudchipLoginFailedError("Login Failed")

        user: model.User = r[0]
        user_volume_type: UserVolumeType = UserValidator.validate_volume_type_by_string(user.volume_type)

        return {
            "static-id": user.static_id,
            "name": user.name,
            "email": user.email,
            "is-admin": user.is_admin,
            "volume-type": {
                "name": user_volume_type.name,
                "value": {
                    "unit": user_volume_type.value[UserVolumeTypeKeys.KEY_TYPE].name,
                    "volume": user_volume_type.value[UserVolumeTypeKeys.KEY_VOLUME]
                }
            }
        }

    # User Control
    def add_user(self, req_static_id: str, data_format: dict):
        # 유저 추가
        """
            req_static_id: 요청을 한 아이디, 절대 새로 생성될 아이디가 아니며
                            오직 Admin 권한만 추가할 수 있다.
        """
        is_accessible = model.User.objects.filter(is_admin=True).filter(static_id=req_static_id)
        if not is_accessible:
            # 해당되지 않는다면 이는 AccessError
            raise MicrocloudchipAuthAccessError("Access for add user Failed")

        # Email 중복 여부 확인
        try:
            model.User.objects.get(email=data_format['email'])
        except model.User.DoesNotExist:
            # 없음 -> 통과
            pass
        else:
            # 있음:
            # Error 출력
            raise MicrocloudchipAuthAccessError("Email Already Exist")

        try:
            user_builder: UserBuilder = UserBuilder() \
                .set_name(data_format['name']) \
                .set_password(data_format['password']) \
                .set_email(data_format['email']) \
                .set_is_admin(False) \
                .set_volume_type(data_format['volume-type'])

        except Exception as e:
            raise e

        # 유저 이미지 Validation 확인
        try:
            if 'img-raw-data' not in data_format or 'img-extension' not in data_format:
                raise KeyError("key not found")
            # 확장자 확인
            if data_format['img-raw-data'] is not None:
                # 생성될 유저 데이터가 들어간 경우
                if data_format['img-extension'] is None:
                    raise MicrocloudchipAuthAccessError("img extension does not exist")
                if data_format['img-extension'] not in self.AVAILABLE_IMG_EXTENSIONS:
                    raise MicrocloudchipAuthAccessError("img extension is not available")

        except KeyError:
            raise MicrocloudchipAuthAccessError("user img data key is not found")

        # 반복되는 static id 가 존재하지 않을 때 까지 반복
        user_builder.set_static_id()
        while True:
            try:
                model.User.objects.get(static_id=user_builder.static_id)
            except model.User.DoesNotExist:
                break
            user_builder.set_static_id()

        # 생성 프로세스
        self.process_locker.acquire()

        # Directory 생성
        new_user_static_id: str = user_builder.static_id
        self.__make_user_directory(new_user_static_id)

        # DB 저장
        user_builder.build().save()

        # User Image 존재하면 user.*** 로 저장
        if data_format['img-raw-data']:
            img_root: str = os.path.join(self.config.get_system_root(), "storage", new_user_static_id, "asset",
                                         f"user.{data_format['img-extension']}")
            with open(img_root, 'wb') as f:
                f.write(data_format['img-raw-data'])

        self.process_locker.release()

    def get_users(self) -> list:
        r = []
        for u in model.User.objects.all():
            r.append(u)
        return r

    def get_user_by_static_id(self, static_id: str) -> dict:
        try:
            d = model.User.objects.get(static_id=static_id)
            return {
                "name": d.name,
                "pswd": d.pswd,
                "email": d.email,
                "is_admin": d.is_admin,
                "volume_type": UserValidator.validate_volume_type_by_string(d.volume_type)
            }
        except model.User.DoesNotExist:
            return None

    def get_used_size(self, static_id: str, zfill_counter: int = 0) -> tuple:

        # 시스템 루트 갖고오기
        sys_root: str = self.config.get_system_root()

        # 해당 유저의 최상위 루트
        super_root: str = os.path.join(sys_root, "storage", static_id, "root")

        r: tuple = (FileVolumeType.BYTE, 0)

        for root, _, files in os.walk(super_root):
            for f in files:
                f_root = os.path.join(root, f)
                f_stat = os.stat(f_root)

                # 파일 용량
                fr: tuple = FileVolumeType.get_file_volume_type(f_stat.st_size)
                r = FileVolumeType.add(r, fr)

        r = FileVolumeType.cut_zfill(r, zfill_counter)
        return r

    def update_user(self, req_static_id: str, data_format: dict):

        # 권한 체크
        try:
            is_accessible = len(model.User.objects.filter(is_admin=True).filter(static_id=req_static_id)) or \
                            data_format['static-id'] == req_static_id

            if not is_accessible:
                raise MicrocloudchipAuthAccessError("Access for update user Failed")
        except KeyError:
            # data format 에 요구되는 key 없는 경으
            raise MicrocloudchipAuthAccessError("Omit key for update user failed")

        # 데이터 갖고오기
        try:
            target_user = model.User.objects.get(static_id=data_format['static-id'])
        except model.User.DoesNotExist:
            # 그새 사라진 경우
            raise MicrocloudchipAuthAccessError("User is not exist")

        # Img Validation

        try:
            if 'img-raw-data' not in data_format or 'img-extension' not in data_format or \
                    'img-changeable' not in data_format:
                raise KeyError("key not found")
            # 확장자 확인
            if data_format['img-raw-data'] is not None:
                # 생성될 유저 데이터가 들어간 경우
                if data_format['img-extension'] is None:
                    raise MicrocloudchipAuthAccessError("img extension does not exist")
                if data_format['img-extension'] not in self.AVAILABLE_IMG_EXTENSIONS:
                    raise MicrocloudchipAuthAccessError("img extension is not available")

        except KeyError:
            raise MicrocloudchipAuthAccessError("user img data key is not found")

        self.process_locker.acquire()

        # 유저 변경
        target_user.name = data_format['name']
        target_user.pswd = data_format['password']
        target_user.volume_type = data_format['volume-type']
        target_user.save()

        # 이미지 변경 여부
        if data_format['img-changeable']:

            asset_root = [self.config.get_system_root(), 'storage', target_user.static_id, 'asset']
            ex: str = ""

            # 이미지 파일 확장자 찾기
            for filename in os.listdir(os.path.join(*asset_root)):
                __splited = filename.split('.')
                if len(__splited) == 2 and __splited[0] == "user":
                    ex = __splited[1]
                    break

            # 이미지 파일이 없는 경우 이미지 파일 생성
            if len(ex) == 0 and data_format['img-raw-data']:
                # 단 img data 가 존재해야 한다.
                with open(os.path.join(*asset_root, f'user.{data_format["img-extension"]}'), 'wb') as f:
                    f.write(data_format['img-raw-data'])
            else:
                # 이미 있는 경우 이전 꺼 삭제하고 새로운 이미지 추가
                os.remove(os.path.join(*asset_root, f'user.{ex}'))

                # raw-data 가 있는 경우 새로운 이미지로 대체한다
                if data_format['img-raw-data']:
                    with open(os.path.join(*asset_root, f"user.{data_format['img-extension']}")) as f:
                        f.write(data_format['img-raw-data'])

        self.process_locker.release()

    def delete_user(self, req_static_id: str, target_static_id: str, storage_manager: StorageManager):

        is_accessible = len(model.User.objects.filter(is_admin=True).filter(static_id=req_static_id))
        if not is_accessible:
            raise MicrocloudchipAuthAccessError("Auth Error for delete user")

        # 자기 자신은 삭제할 수 없다.
        if req_static_id == target_static_id:
            raise MicrocloudchipAuthAccessError("User can't remove itself")

        # Storage 제거
        self.process_locker.acquire()
        try:
            storage_manager.delete_directory(target_static_id, {
                'static-id': target_static_id,
                'target-root': ''
            })

            # 기타 유저 데이터 삭제
            user_root = os.path.join(self.config.get_system_root(), 'storage', target_static_id)
            shutil.rmtree(user_root)
        except Exception as e:
            self.process_locker.release()
            raise e
        self.process_locker.release()
