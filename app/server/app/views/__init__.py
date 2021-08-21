# Global Variable 불러오기
""" global variables """
from module.specification.System_config import SystemConfig
from module.manager.user_manager import UserManager
from module.manager.storage_manager import StorageManager

SYSTEM_CONFIG = SystemConfig("server/config.json")
USER_MANAGER = UserManager(SYSTEM_CONFIG)
STORAGE_MANAGER = StorageManager(SYSTEM_CONFIG)
