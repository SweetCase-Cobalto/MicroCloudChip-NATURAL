# MicroCloudChip-NATURAL

![](readme-asset/title.png)
<center>
<img alt="GitHub release (latest by date including pre-releases)" src="https://img.shields.io/github/v/release/SweetCase-Cobalto/MicroCloudChip-NATURAL?include_prereleases&style=for-the-badge">
</center>
<center>
<a href="https://seokbong60.gitbook.io/microcloudchip-natural/">
<img alt="gitbook site" src="https://img.shields.io/badge/GitBook-7B36ED?style=for-the-badge&logo=gitbook&logoColor=white">
</a>
<a href="https://hub.docker.com/repository/docker/recomadock/microcloudchip-natural">
<img alt="" src="https://img.shields.io/badge/Docker Hub-2CA5E0?style=for-the-badge&logo=docker&logoColor=white">
</a>
</center>



# 개요
* 전 작 [MicroCloudChip](https://github.com/SweetCase-Cobalto/MicroCloudChip) 의 후속작
* 원격 서버 및  NAS Server의 파일 관리 서비스를 지원하기 위해 개발된 설치형 저용량 파일 호스팅 서비스
* 타 서버로부터 금액을 지불하고 일정 용량을 할당 받는 것이 아닌, 개인 서버만 갖고 있으면 이 웹 어플리케이션을 이용해 파일 호스팅 서버를 운용할 수 있습니다.
* Docker Image를 사용하여 설치를 할 경우 Docker Container 밖 Directory를 마운팅 할 수 있기 때문에 ```docker run``` 명령어에 Directory root 환경 변수와 ```-v``` Flag 설정만 해주면 불가피하게 Container가 Shutdown이 되어도 파일 접근이 가능합니다.
* Database도 외부 MySQL같은 Database를 사용할 수 있습니다 (v0.1.x 에 추가 구현 예정)

# Available Platform
## Current Available ![](https://img.shields.io/badge/version-0.0.x-blue?style=flat-square)
|OS|Database|
|---|---|
|![debian](https://img.shields.io/badge/Debian-A81D33?style=for-the-badge&logo=debian&logoColor=white)|![sqlite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)|
## Will be Available in next version ![](https://img.shields.io/badge/version-0.1.x-brightgreen?style=flat-square)
|OS|Database|
|---|---|
|![windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)|![mysql](https://img.shields.io/badge/MySQL-00000F?style=for-the-badge&logo=mysql&logoColor=white)|
||![](https://img.shields.io/badge/MariaDB-003545?style=for-the-badge&logo=mariadb&logoColor=whit)|
* In Windows, This Application can run only Testing (No Service)

# Technology stacks
|position|Technology Stacks|
|---|---|
|Frontend|![Javascript](https://img.shields.io/badge/JavaScript(Node)-14.x-323330?style=flat-square&logo=javascript&logoColor=F7DF1E&color=yellow) ![React](https://img.shields.io/badge/React-17.x-20232A?style=flat-square&logo=react&logoColor=61DAFB) ![Redux](https://img.shields.io/badge/Redux-593D88?style=flat-square&logo=redux&logoColor=white) ![bootstrap](https://img.shields.io/badge/Bootstrap-5.x-563D7C?style=flat-square&logo=bootstrap&logoColor=white)|
|Backend|![Python](https://img.shields.io/badge/Python-3.9.x-3776AB?style=flat-square&logo=python&logoColor=white) ![DJango](https://img.shields.io/badge/Django-3.2.x-092E20?style=flat-square&logo=django&logoColor=green) ![perl](https://img.shields.io/badge/Perl-5.x-39457E?style=flat-square&logo=perl&logoColor=white)|
|database(available)|![sqlite](https://img.shields.io/badge/SQLite-07405E?style=flat-square&logo=sqlite&logoColor=white) ![mysql](https://img.shields.io/badge/MySQL-00000F?style=flat-square&logo=mysql&logoColor=white) |
|Installer|![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=flat-square&logo=docker&logoColor=white) ![Perl](https://img.shields.io/badge/Perl-39457E?style=flat-square&logo=perl&logoColor=white)|

# Installation
## For Users
## For Developers
이 프로젝트를 개작 또는 분석 하려는 개발자를 위한 세팅 방법입니다.(정확히는 "설치 방법"이 아니지만 )