---
description: Task Manager들 선언 위치
---

# Manager Init Location

Application 의 작업을 담당하는 Manager들은 api를 작성하는 views디렉토리의 init.py에 위치해 있습니다. view 의 api method에서 Manager를 이용해 작업을 처리하기 때문에 global variable 형태로 저장되어 있습니다.

```python
# Global Variable 불러오기
""" global variables """
import django.db.utils
from django.db import OperationalError

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
except (OperationalError, django.db.utils.ProgrammingError) as e:
    pass
```

* line 21: OperationalError, django.db.utils.ProgrammingError 에러가 발생했을 경우, 에러 호출 및 기타 작업이 아닌 pass로 처리되어 있습니다. 그 이유는 **Unittest 및 migration을 진행할 때,  Database에 model에 해당하는 table이 존재하지 않아 발생하는 에러를 suppress 함으로써 정상적인 테스트 진행을 하기 위함입니다.**

****
