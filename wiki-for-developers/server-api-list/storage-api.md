---
description: 스토리지(파일/디렉토리) 관련 API Wiki
---

# Storage API

{% swagger baseUrl="http(s)://[server-host]:[server-port]" path="/server/storage/data/file/:user/:root" method="post" summary="Upload File" %}
{% swagger-description %}
파일 업로드 하기
{% endswagger-description %}

{% swagger-parameter in="path" name="root" type="string" %}
target directory that file will be uploaded
{% endswagger-parameter %}

{% swagger-parameter in="path" name="user" type="string" %}
target user static id
{% endswagger-parameter %}

{% swagger-parameter in="header" name="Set-Cookie" type="string" %}
token
{% endswagger-parameter %}

{% swagger-parameter in="body" name="file" type="string" %}
uploaded file
{% endswagger-parameter %}

{% swagger-response status="200" description="return 0 if success" %}
```
{ code: [integer] }
```
{% endswagger-response %}
{% endswagger %}

{% swagger baseUrl="http(s)://[server-host]:[server-port]" path="/server/storage/data/file/:user/:root" method="get" summary="Get File Info" %}
{% swagger-description %}
 파일 정보 갖고오기 (Raw Data 제외)
{% endswagger-description %}

{% swagger-parameter in="path" name="user" type="string" %}
target user
{% endswagger-parameter %}

{% swagger-parameter in="path" name="root" type="string" %}
target file root
{% endswagger-parameter %}

{% swagger-parameter in="header" name="Set-Cookie" type="string" %}
token
{% endswagger-parameter %}

{% swagger-response status="200" description="" %}
```
{
    code: 0,
    data: {
        create-date: YYYY/MM/DD HH:MM:SS,
        modify-date: YYYY/MM/DD HH:MM:SS,
        file-name: [file name],
        file-type: [TEXT, IMAGE, AUDIO, ETC...],
        size: {
            size-type: [KB, MB, ETC...],
            size-volume: [float]
        }
    }
}
```
{% endswagger-response %}
{% endswagger %}

{% swagger baseUrl="http(s)://[server-host]:[server-port]" path="/server/storage/data/file/:user/:root" method="patch" summary="Modify File Info" %}
{% swagger-description %}
 파일 정보 수정

\


수정 내역

\


1\. 파일 이름
{% endswagger-description %}

{% swagger-parameter in="path" name="user" type="string" %}
target user
{% endswagger-parameter %}

{% swagger-parameter in="path" name="root" type="string" %}
target file root
{% endswagger-parameter %}

{% swagger-parameter in="header" name="Set-Cookie" type="string" %}
token
{% endswagger-parameter %}

{% swagger-parameter in="body" name="filename" type="string" %}
new filename
{% endswagger-parameter %}

{% swagger-response status="200" description="if success return code 0" %}
```
{ code: [integer] {
```
{% endswagger-response %}
{% endswagger %}

{% swagger baseUrl="http(s)://[server-host]:[server-port]" path="/server/storage/data/file/:user/:root" method="delete" summary="Delete File" %}
{% swagger-description %}
 파일 삭제
{% endswagger-description %}

{% swagger-parameter in="path" name="user" type="string" %}
target user
{% endswagger-parameter %}

{% swagger-parameter in="path" name="root" type="string" %}
target directory that file will be uploaded
{% endswagger-parameter %}

{% swagger-parameter in="header" name="Set-Cookie" type="string" %}
token
{% endswagger-parameter %}

{% swagger-response status="200" description="if success then return 0" %}
```
{ code: [integer] }
```
{% endswagger-response %}
{% endswagger %}

{% swagger baseUrl="http(s)://[server-host]:[server-port]" path="/server/storage/data/dir/:user/:root" method="post" summary="Generate Directory" %}
{% swagger-description %}
 디렉토리 생성
{% endswagger-description %}

{% swagger-parameter in="path" name="root" type="string" %}
new directory root
{% endswagger-parameter %}

{% swagger-parameter in="path" name="user" type="string" %}
target user
{% endswagger-parameter %}

{% swagger-parameter in="header" name="Set-Cookie" type="string" %}
token
{% endswagger-parameter %}

{% swagger-response status="200" description="if success then return 0" %}
```
{ code: [integer] }
```
{% endswagger-response %}
{% endswagger %}

{% swagger baseUrl="http(s)://[server-host]:[server-port]" path="/server/storage/data/dir/:user/:root" method="patch" summary="Modify Directory" %}
{% swagger-description %}
 디렉토리 정보 수정
{% endswagger-description %}

{% swagger-parameter in="path" name="user" type="string" %}
target user
{% endswagger-parameter %}

{% swagger-parameter in="path" name="root" type="string" %}
target directory
{% endswagger-parameter %}

{% swagger-parameter in="header" name="Set-Cookie" type="string" %}
token
{% endswagger-parameter %}

{% swagger-parameter in="body" name="dir-name" type="string" %}
new directory name
{% endswagger-parameter %}

{% swagger-response status="200" description="return 0 if success" %}
```
{ code: [integer] }
```
{% endswagger-response %}
{% endswagger %}

{% swagger baseUrl="http(s)://[server-host]:[server-port]" path="/server/storage/data/dir/:user/:root" method="get" summary="Get Directory Info" %}
{% swagger-description %}
 디렉토리 정보 갖고오기(Raw Data 제외)
{% endswagger-description %}

{% swagger-parameter in="path" name="user" type="string" %}
target user
{% endswagger-parameter %}

{% swagger-parameter in="path" name="root" type="string" %}
target directory root
{% endswagger-parameter %}

{% swagger-parameter in="header" name="Set-Cookie" type="string" %}
token
{% endswagger-parameter %}

{% swagger-response status="200" description="if success then return code 0 and data" %}
```
{
    code: 0,
    data: {
        info: {
            create-date: YYYY/MM/DD HH:MM:SS,
            modify-date: YYYY/MM/DD HH:MM:SS,
            dir-name: [directory name],
            file-size: [size of file]
        },
        list: {
            file: [
                {fileinfo}, {}, ...
            ],
            dir: [
                {dirinfo}, {}, ...
            ]
        }
    }
}
```
{% endswagger-response %}
{% endswagger %}

{% swagger baseUrl="http(s)://[server-host]:[server-port]" path="/server/storage/data/dir/:user/:root" method="delete" summary="Delete Directory (Recursive)" %}
{% swagger-description %}
  디렉토리 삭제하기
{% endswagger-description %}

{% swagger-parameter in="path" name="user" type="string" %}
target user
{% endswagger-parameter %}

{% swagger-parameter in="path" name="root" type="string" %}
target directory root
{% endswagger-parameter %}

{% swagger-parameter in="header" name="Set-Cookie" type="string" %}
token
{% endswagger-parameter %}

{% swagger-response status="200" description="return 0 if success" %}
```
{ code: 0 }
```
{% endswagger-response %}
{% endswagger %}
