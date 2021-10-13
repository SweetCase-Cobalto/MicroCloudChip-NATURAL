---
description: 개발 환경 구성
---

# Project Setting

## In Windows

powershell을 사용합니다.

1. Install Package
   1. install python (over 3.9.x)
   2. install nodejs (over 14.x)
   3. install perl _(설정 파일이나 기타 필수 텍스트 파일을 생성하기 위해 설치합니다.)_
2.  download respository

    ```
        PS X:\> git clone https://github.com/SweetCase-Cobalto/MicroCloudChip-NATURAL.git
    ```
3.  Install python & nodejs packages

    ```
        PS: X:\> cd project
        PS: X:\project> cd web
        PS: X:\project/web> npm i
        PS: X:\project> cd ..
        # 파이썬 가상머신을 설치했다고 가정합니다
        PS: (micro)X:\project> cd app
        PS: (micro)X\project\app> pip install -r requirements.txt
    ```

    _**NOTE:**_ Backend package를 설치할 때 `pip upgrade`를 해놓을 경우 package 설치에 문제가 있으니 `pip upgrade`를 수행하지 않는 것을 권장합니다.
4. write config.json
   * config.json 은 Microcloudchip-NATURAL이 실행을 하기 위해 참고하는 설정 파일입니다. 어플리케이션을 설치할 때는 자동으로 생성해 주지만, 개발 단계에서는 perl script를 사용하여 직접 세팅해야 합니다.
   *   내부 데이터베이스(Sqlite3를 사용하는 경우)

       ```
       PS: X:\project> cd bin
       PS: X:\project/bin> perl setConfigure-sqlite.pl [storage root] [port] [host] [email]
       ```
   *   외부 데이터베이스(MySQL, MariaDB)를 사용하는 경우 _(0.1.x 부터 개발 가능합니다.)_

       ```
       PS: X:\project> cd bin
       PS: X:\project/bin> perl setConfigure-sqlite.pl [storage root] [port] [host] [email] `
       >> [db-host] [db-port] [db-user-name] [db-user-pswd] [db-name]
       ```
