---
description: 예외처리를 간편하게 해주는 에러 코드 리스트
---

# Error Code List

## 개요

Error Code를 한번에 모아보는 사전입니다.

해당 링크에서 실제로 구현된 Error Exception을 보실 수 있습니다.

## System Error

System Error의 접두사는 0x00 00 00 00 입니다.

| Error Name                    | Code          | Summary                                                |
| ----------------------------- | ------------- | ------------------------------------------------------ |
| SystemConfigFileNotFoundError | 0x00 00 00 01 | Sytem Config.json 파일 찾기 실                              |
| SystemConfigFileParsingError  | 0x00 00 00 02 | System config.json 파일의 데이터가 잘못되었거나  찾지 못한 경우에 대한 Error |
| SystemAbnormalAccessError     | 0x00 00 00 03 | 비정상 접근 에                                               |
| LoginConnectionExpireError    | 0x00 00 00 04 | 로그인 만료 에러                                              |

## User Error

User Error의 접두사는 0x01 00 00 00 입니다

| Error Name                                 | Code          | Summary                      |
| ------------------------------------------ | ------------- | ---------------------------- |
| <p>UserInformationValidateErro</p><p>r</p> | 0x01 00 00 01 | 잘못된 요청 데이터로 인해 사용자 등록 및 수정 실 |
| UserUploadFailedError                      | 0x01 00 00 02 | 사용자 이미지 업로드 실                |
| UserDoesNotExistError                      | 0x01 00 00 03 | 유저를 찾을 수 없을 때 발생하는 에         |
| LoginFailedError                           | 0x01 00 00 04 | 로그인 실패                       |

## Data Error

Data(Storage) 관련 접두사는 0x02 00 00 00 입니다

| Error Name                           | Code          | Summary                      |
| ------------------------------------ | ------------- | ---------------------------- |
| DirectoryNotFound                    | 0x02 00 00 01 | 디렉토리가 존재하지 않음                |
| FileNotFound                         | 0x02 00 00 02 | 파일이 존재하지 않음                  |
| FileAndDirectoryNameValidateError    | 0x02 00 00 03 | 파일 및 디렉토리 이름이 유효하지 않음        |
| DirectoryAleadyExistError            | 0x02 00 00 04 | 디렉토리 생성 시 이미 존재할 경우 에러 발     |
| FileAleadyExistError                 | 0x02 00 00 05 | 파일 추가 및 생성 시에 이미 존재할 경우 에러 발 |
| StorageOverCapacityError             | 0x02 00 00 06 | 용량 초과                        |
| DirectoryDeleteFailedBecauseSomeData | 0x02 00 00 07 | 디렉토리에 아직 데이터가 남아 있어서 삭제 못함   |
| FileAndDirectoryNameEmpty            | 0x02 00 00 07 | 디렉토리 및 이름이 비어있               |

## Access Error

Access관련 접두사는 0x03 00 00 01 입니다.

| Error Name      | Code          | Summary   |
| --------------- | ------------- | --------- |
| AuthAccessError | 0x03 00 00 01 | 권한 엑세스 에러 |
