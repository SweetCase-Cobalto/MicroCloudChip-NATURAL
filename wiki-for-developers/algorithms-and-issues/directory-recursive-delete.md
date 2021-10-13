---
description: 디렉토리 순환 삭제 알고리즘
---

# Directory Recursive Delete

## 개요

디렉토리를 삭제할 때 파일 이 있다면 파일부터 삭제하고, 하위 디렉토리가 있으면 그 디렉토리에 들어가서 삭제를 해야 합니다. Python 자체 디렉토리 순환 삭제 함수로  `rmtree()` 도 있지만 각 파일이나 디렉토리에 특정 플래그(공유 설정 등...)이 있으면 삭제 전 플래그들을 지우는 것이 불가능하기 때문에 따로 알고리즘을 구현할 필요가 있었습니다.

## Algorithm

* 종류
  * DFS 알고리즘을 사용합니다.

1. 순서
   1. stack에서 가장 위에 있는 디렉토리 루트를 참조합니다 (pop()이 아닌 \[-1])
   2. 현재 위치의 디렉토리에서 파일 리스트와 디렉토리 리스트를 가져옵니다.
   3. 현재 위치의 파일들을 삭제합니다.
   4. 파일 삭제 후 디렉토리가 남아있는 지 확인합니다.
      1. 남아있다면 하위 디렉토리 루트들을 순환 탐색하기 위해 stack에 추가합니다.
      2. 남아있지 않다면 현재 디렉토리를 stack에서 꺼냅니다.
   5. 1 \~ 4번을 stack이 비어있을 때 까지 반복합니다.

## In Builder/Format Layer

Builder/Format Layer에서는 디렉토리를 지울 경우 디렉토리 안에 파일 및 하위 디렉토리가 남아있다면 에러를 호출합니다. 그 이유는, 이 계층에서는 오로지 자기 자신의 데이터만 관리를 해야 하는데 해당 디렉토리 및 파일을 건드린 다는 것은 다른 객체의 영역에 침범하는 것이기 때문에 이 때 Error를 호출합니다. [참고](https://github.com/SweetCase-Cobalto/microcloudchip-natural/blob/master/app/server/module/data/storage_data.py#L264-L281)

```python
    def remove(self):
        # 디렉토리 삭제
        # 단 data 단에서의 삭제는 디렉토리 안에 아무것도 없어야 한다.
        super().remove()
        self.__call__()
        if os.path.isdir(self.full_root):
            # 디렉토리가 존재하는 지 확인
            if len(os.listdir(self.full_root)) == 0:
                # 디렉토리가 비어있는 경우 삭제
                os.rmdir(self.full_root)
                # 디렉토리가 없기 때문에 is_called를 False 처리한다.
                self.is_called = False
            else:
                self.is_called = True
                raise MicrocloudchipDirectoryDeleteFailedBacauseOfSomeData(
                    "Directory delete failed because of some data")

        self.is_called = False
```

 따라서 디렉토리 순환 삭제는 Storage Manager에서 담당합니다.

## In Manager Layer

Storage Manger에서 delete_directory를 이용하여 디렉토리 순환 삭제를 할 수 있습니다. DFS 알고리즘을 진행할 때 Recursive 관련 Exception을 예방하기 위해 제귀함수가 아닌 stack을 사용합니다. [참고](https://github.com/SweetCase-Cobalto/microcloudchip-natural/blob/master/app/server/module/manager/storage_manager.py#L343-L383)

```python
try:

    stack = [target_root]

    while stack:
        r = stack[-1]

        # Full Real Root
        full_r = os.path.join(self.config.system_root, "storage",
                              target_static_id, "root", self.TOKEN.join(r.split('/')))

        f_list, d_list = self.get_dirlist(req_static_id, {
            "static-id": target_static_id,
            'target-root': r
        })

        # 파일 부터 죄다 삭제
        for f in f_list:
            self.delete_file(req_static_id, {
                'static-id': target_static_id,
                'target-root': f"{r}/{f.name}",
            }, share_manager)

        # 파일을 전부 삭제하고 디렉토리가 없는 경우
        # 그냥 현재 디렉토리를 삭제한다
        if len(d_list) == 0:
            stack.pop()
            # get full root

            deleted_d: DirectoryData = DirectoryData(full_r)()
            deleted_d.remove()
        else:
            # 루트 를 더하고 스택에 추가
            # POP 을 하지 않는 이유는 모든 모든 디렉토리가 없는 경우 대해 한 번 더 함수를 실행해서
            # 루트 자체를 삭제하기 위해
            for d in d_list:
                next_r = f"{r}/{d.name}"
                stack.append(next_r)

except Exception as e:
    raise e
```

* line 3: stack에 삭제 대상 디렉토리 루트를 추가합니다.
* line 9: 클라이언트로부터 받은 상대적 루트를 스토리지 탐색을 위해 절대적 루트로 전환합니다.
* line 12: get_dirlist 함수를 사용하여 해당 디렉토리에 존재하는 파일과 디렉토리를 Format Layer 형태로 가져옵니다.
* line 18 - 22: 파일 리스트를 순환하여 파일을 하나 씩 삭제합니다. 이 때 SharedManager로 parameter로 추가하여 **공유 상태를 확인하여 공유되어있을 경우, 해제한 다음 파일을 삭제합니다.**
* line 26 - 27: 하위 디렉토리 존재 여부를 확인하여 비어있는 참조했었던 현재 디렉토리 루트를 stack에서 꺼내 소멸시킵니다.
* line 28 \~ 30: 그런 다음 현재 디렉토리를 스토리지에서 삭제합니다.
* line 32 \~ 38: 비어있지 않은 경우 stack에 하위 디렉토리를 추가합니다.
