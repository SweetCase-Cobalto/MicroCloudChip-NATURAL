---
description: 공유 기한 만료 모니터링 알고리즘
---

# Expired Of Sharing Monitoring

## 개요

클라우드에 저장된 파일을 다른 사람들에게 공유하기 위해** 0.1.0 버전에 공유 기능이 추가되었습니다.** 공유 기간은 약 7일로(정식 버전에서는 관리자가 직접 기한을 선택하는 방향으로 변경될 수 있음) 이 기한이 지나면 공유는 자동으로 해제되고 이 때 외부 클라이언트는 접근할 수 없게 됩니다.

## 이슈

* 일정 기간이 지난 데이터들은 DB에서 자동으로 지워져야 합니다.
* Database의 Trigger를 고려해 봤으나 Trigger는 외부에서 작업이 들어올 대 실행되는 방식이므로 이를 시간 간격으로 Database를 접근하는 것은 비용이 많이 들 수 있습니다.
  * 뿐만 아니라 SQLite일 경우 오직 하나의 스레드 만 파일을 접근할 수 있게 설정되어 있기 때문에 상당한 성능 저하가 예상됩니다.
* 이러한 이유로 데이터베이스를 최소한으로 접근하고 가장 프로세스를 적게 사용하면서 정상적인 기능 작동을 고려해야 합니다.

## 해결

### Algorithm

* 사용되는 알고리즘 종류
  * 우선순위 큐(Heap)

1. 일정 시간 간격으로 DB로부터 공유 데이터를 받습니다.  그러나 모든 데이터를 받는 것이 아니라 **만료 시간**이 **다음 DB로부터 데이터를 받는 시간 전** 이어야 합니다.
2. 공유 데이터 만료를 처리하는 우선순위 큐에 삽입합니다. 이 때 우선순위의 기준은 **만료 시간**으로 가장 **먼저 만료되는 공유 데이터** 순으로 정렬됩니다.
3. 1 ms 간격으로 맨 앞에 있는 공유 데이터의 만료시간을 체크하여 시간이 다 되면 꺼내 공유 데이터를 소멸시킵니다. 1번을 수행할 시간이 될 때 까지 3번을 반복합니다.
4. 1번과 3번을 계속 반복합니다.

### 특징 및 장점

* **특징**
  * 알고리즘 순서에서는 만료시간 이라고 나타냈지만  Database 상의 ShareFileData의 Attribute에서는 만료 시간이 아닌 **공유 설정 시간이 설정되어 있습니다.  **하지만 공유 기한은 ShareManager에서 설정되어 있기 때문에 만료 시간 계산법은 다음과 같습니다.
    * 만료 시간 = 공유 설정 시간 + 공유 기한
  * DB로부터 받는 시간 간격은 공유 기한이 **1일 이상일 경우 1일**, 그 이하일 경우 **공유 기한의 1/10**로 자동 설정됩니다. 다음 DB로부터 받는 시간 전 까지 만료가 되는 데이터들만 받아와야 하는데 이에 대한 계산법은 다음과 같습니다

![](<../../.gitbook/assets/image (28).png>)

* 변수
  * n(now) = DB로부터 데이터를 받은 시간
  * i(interval) = DB Access 시간 간격
  * l(limit) = 공유 기한

$$
f(n, i, l) = n + i - l
$$

* **장점**
  * DB로부터 데이터를 받아올 때 모든 데이터를 받는 것이 아닌 **다음 턴 안에 만료되는 공유 데이터**만 받아옵니다. 따라서 다음 턴 사이에 공유 데이터가 삭제/변경/생성되어도 중간에 새로 생성된 공유 데이터를 큐에 삽입하던가 **중간에 큐에 작업하는 일은 없습니다.**
    * 공유되는 데이터가 변경(파일 이름 등)되더라도 **Shared Data의 Primary key는 shared id**입니다. 따라서 데이터가 변경되어도 shared id는 변하지 않는데다 해당 큐의 용도는 만료 기한만 체크하기 때문에 큐에 추가작업하는 일은 없습니다.
    * 공유되는 데이터가 중간에 삭제되거나 공유 해제되어도 해당 작업이 된 데이터를 뽑아서 DB에 삭제 요청을 하기 전에 한번 더 검증을 거치기 때문에 아무런 문제가 없을 뿐더러, 먼저 만료된 순서대로 정렬이 되어 있기 때문에 어차피 가장 맨 앞에 있는 데이터가 만료 될 때 까지 뒤에 있는 공유 데이터들은 만료 처리가 되지 않습니다. 따라서 추가 작업을 할 필요가 없습니다.
  * **먼저 만료되는 순으로 정렬되어 있습니다. **맨 앞의 데이터가 만료가 되지 않으면 뒤에 있는 데이터도 만료되지 않습니다. 따라서 For문을 사용하여 만료 시간을 체크할 필요도 없이 **맨 앞에 있는 데이터만 체크하면 됩니다.**

### Code Review ([코드 참고](https://github.com/SweetCase-Cobalto/microcloudchip-natural/blob/master/app/server/module/manager/share_manager.py#L135-L204))

#### 초기 설정 (변수 선언)

```python
    def __thread_process(self):
        # Application Sub Thread

        # 만료 대상 Shared File List (Heap)
        expired_shareds: List[(datetime.datetime, str)] = []

        thread_timers = {"refreshed-time": datetime.datetime.now(), "is-first": True}
        if self.time_limit >= datetime.timedelta(days=1):
            # 1일 이상일 경우 1일로 측정
            thread_timers['time-delta'] = datetime.timedelta(days=1)
        else:
            # 1일 이하일 경우 유효기간의 10일로 책정
            thread_timers['time-delta'] = self.time_limit / 10

        # 다음 새로고침 대상 시간
        # 처음엔 바로 작동해야 하므로 now로 설정
        thread_timers['next-refresh-time'] = thread_timers['refreshed-time']
```

* expired_shareds: 만료 대상 공유 데이터가 들어가는 Queue 입니다.
  * index 0: 만료 시간이 들어갑니. 이 만료시간이 우선순위 큐의 기준이 됩니다.
  * index 1: 공유 파일의  shared_id 입니다.
* refreshed-time: DB Access가 수행되었던 시간입니다. 초기 설정에서는 바로 DB에 접근해야 하기 때문에 지금 시간으로 설정합니다.
* time-delta: DB Access 시간 간격 입니다.
* next-refresh-time: 다음 DB에 접근 할 예약 시간 입니다. refreshed-time 처럼 시작하자마자 DB에 접근해야 하므로 refreshed-time과 일치하게 선언합니다.

#### DB Access Routine (refresh())

```python
def refresh():
    # timer update
    thread_timers["refreshed-time"] = datetime.datetime.now()
    thread_timers['next-refresh-time'] = thread_timers['refreshed-time'] + thread_timers['time-delta']

    # 다음 리프레시 시간 전에 만료될 Shared File 갖고오기
    self.process_locker.acquire()
    try:
        end_time = thread_timers['refreshed-time'] + thread_timers['time-delta'] - self.time_limit

        expired_list: List[model.SharedFile] = \
            SharedFileData.get_shared_file_for_shared_manager_queue(
                self.config.get_system_root(), end_time)

    except Exception as e:
        self.process_locker.release()
        raise e
    else:
        if self.process_locker.locked():
            self.process_locker.release()
    while expired_list:
        expired_data: model.SharedFile = expired_list.pop()

        # 일찍 만료되는 순으로 정렬
        heapq.heappush(expired_shareds, (expired_data.start_date + self.time_limit, expired_data.shared_id))
```

DB에 Access 해서 공유 만료 대상 데이터를 수집합니다.

* line 3 \~ 4: 타이머를 초기화합니다
  * refreshed-time: DB Access를 하기 시작했으므로 지금 시간으로 설정합니다.
  * next-refresh-time: 다음 DB Access 시간을 설정합니다.
    * self.time_limit은 공유 기한으로 refreshed-time에 self.time limit을 더해서 next-refresh-time을 구합니다.
* line 7: DB에 Access 해야 하므로 데이터 충돌 방지를 위해 Thread에 Lock을 걸어놓읍니다.
* line 8: 다음 DB에 Access하기 전 까지 만료되는 데이터를 수집하기 위해 가장 늦게 만료되는 공유 시작 시간을 구합니다. 이렇게 구한 변수 end time은 아래와 같이 쿼리로 구성됩니다. [참고](expired-of-sharing-monitoring.md#undefined-2)
  * 여기서 \__lte는 `<=` (작거나 같음) 를 의미합니다. 따라서 end time보다 더 이른 공유 시간을 가진 데이터를 수집하게 됩니다.

```python
model.SharedFile.objects.filter(start_date__lte=end_date):
```

* line 11 \~ 13: 만료 대상 공유 데이터들을 수집합니다.
* line 15 \~ 20: 문제가 생길 경우 에러를 호출하고 그렇지 않은 경우 그냥 패스합니다. 물론 이전에 Lock 걸어둔 부분은 다시 해제합니다.
* line 21 \~ 25: 만료 대상 리스트에서 데이터를 하나 씩 뽑아서 먼저 만료되는 순으로 heapq를 사용하여 우선순위 큐에 추가합니다.

#### All Routine

```python
while True:
    now: datetime.datetime = datetime.datetime.now()

    # Refresh 타임 측정 및 진행
    if now >= thread_timers['next-refresh-time']:
        try:
            refresh()
        except Exception as e:
            raise e
    else:
        # 만료 모니터링
        if expired_shareds:
            if expired_shareds[-1][0] < now:
                # 만료되었음
                _, shared_id = heapq.heappop(expired_shareds)
                try:
                    shared_data = SharedFileData(shared_id=shared_id, system_root=self.config.system_root)()
                    shared_data.unshare()
                except MicrocloudchipException:
                    pass

    time.sleep(self.thread_sleep_long)
```

* line 2: 현재 시간을 갖고옵니다.
* line 5 \~ 9: DB에 Access 해야 할 시간이 되면 refresh()롤 호출하여 DB에 Access하여 데이터를 수집합니다.
* line 10: 아직 시간이 안된 경우 계속해서 만료 시간을 체킹합니다.
* line 13: 큐의 맨 앞의 데이터의 만료시간이 다 되었는지 측정합니다.
* line 15: 만료 시간이 다 되었다면 shared_id를 뽑아와서 공유데이터를 삭제할 준비를 합니다.
* line 17: 공유 데이터 삭제를 위해 shared_id를 이용해 Format Layer의 SharedFileData를 생성합니다.
* line 18: 공유를 해제합니다.
* line 19: 파일이 없거나 이미 공유가 해제된 이유로 Exception을 호출 한 경우가 있습니다. 이미 삭제가 되어 졌을 뿐 시스템에 아무런 영향을 미치지 않으므로  pass 처리합니다.
* line 22: 1ms 간격으로 쓰레드가 작동합니다.
