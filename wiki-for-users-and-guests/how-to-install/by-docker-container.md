---
description: Docker를 이용한 설치
---

# By Docker Container

## Docker ENVS

* **\[필수]** SERVER_PORT: 서버와 통신 할 포트를 지정합니다
* **\[필수]** ADMIN_EMAIL: Admin Email를 설정합니다
* **\[필수]** HOST: Container를 생성하는 고정 IP를 설정합니다. 고정IP 대신 127.0.0.1를 설정하면 자기 자신만 접속할 수 있습니다.
* STORAGE_ROOT: 사용자의 파일 및 디렉토리나 기타 asset 파일을 저장하는 장소를 지정합니다. 주로 외부 저장소를 활용할 때 사용합니다.

## 설치 시 주의할 점 

{% hint style="warning" %}
`docker run` 을 진행하면 바로 Container가 세팅되지 않습니다. 그 이유는 React Code를 정적파일로 만드는 과정을` docker run`에서 진행하게 되는데 `npm i` 명령어를 이용한 node module을 설치하는 데 시간이 걸리기 때문입니다. 따라서, 컨테이너를 생성 한 다음, `npm logs [container name]` 명령어를 반복적으로 입력하여 컨테이너 세팅 여부를 확인해야 합니다.
{% endhint %}

## 내부 Database를 사용하는 경우 

{% hint style="info" %}
 tag는 크게 Internal과 mysql 두 가지로 나뉘며 internal은 내부 DB를 사용하는 경우를 말합니다(Sqlite3)
{% endhint %}

 내부 저장소를 사용할 경우 아래와 같이 docker run 을 진행합니다

```bash
sudo docker run -it -d -p [port]:[port] \
                -e SERVER_PORT=[port] \
                -e ADMIN_EMAIL=[your email] \
                -e HOST=[your host] \
                --name [container name] ghcr.io/sweetcase-cobalto/microcloudchip-natural:0.1.0.beta1-internal
```

외부 저장소를 사용할 경우 아래와 같이 진행 합니다.

```
sudo docker run -it -d -p [port]:[port] \
                -v [src]:[dst] \
                -e STORAGE_ROOT=[dst] \
                -e SERVER_PORT=[port] \
                -e ADMIN_EMAIL=[your email] \
                -e HOST=[your host] \
                --name [container name] ghcr.io/sweetcase-cobalto/microcloudchip-natural:0.1.0.beta1-internal
```

##  외부 데이터베이스 (Mysql, MariaDB)를 사용하는 경우

부 저장소를 사용하는 경우 

```bash
sudo docker run -it -d -p [port]:[port] \
                -v [src]:[dst] \
                -e STORAGE_ROOT=[dst] \
                -e SERVER_PORT=[port] \
                -e ADMIN_EMAIL=[your email] \
                -e HOST=[your host] \
                -e DB_NAME=[database name] \
                -e DB_USER=[database user name] \
                -e DB_PSWD=[database password] \
                -e DB_HOST=[database host] \
                -e DB_PORT=[database port] \
                --name [container name] ghcr.io/sweetcase-cobalto/microcloudchip-natural:0.1.0.beta1-mysql
```

부 저장소를 사용하는 경우 

```bash
sudo docker run -it -d -p [port]:[port] \
                -e SERVER_PORT=[port] \
                -e ADMIN_EMAIL=[your email] \
                -e HOST=[your host] \
                -e DB_NAME=[database name] \
                -e DB_USER=[database user name] \
                -e DB_PSWD=[database password] \
                -e DB_HOST=[database host] \
                -e DB_PORT=[database port] \
                --name [container name] ghcr.io/sweetcase-cobalto/microcloudchip-natural:0.1.0.beta1-mysql
```
