# Global Variable 불러오기
""" global variables """
from django.db import OperationalError

from module.manager.token_manager import TokenManager
from module.specification.System_config import SystemConfig
from module.manager.user_manager import UserManager
from module.manager.storage_manager import StorageManager
from module.manager.token_manager import TokenManager

SYSTEM_CONFIG: SystemConfig
USER_MANAGER: UserManager
STORAGE_MANAGER: StorageManager
TOKEN_MANAGER: TokenManager

try:
    SYSTEM_CONFIG = SystemConfig("server/config.json")
    USER_MANAGER = UserManager(SYSTEM_CONFIG)
    STORAGE_MANAGER = StorageManager(SYSTEM_CONFIG)
    TOKEN_MANAGER = TokenManager(SYSTEM_CONFIG, 1200)
except OperationalError:
    pass
