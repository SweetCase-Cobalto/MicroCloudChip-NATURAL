---
description: 파일을 직접적으로 다운로드 해주는 API 리스트
---

# Download API

{% swagger baseUrl="http(s)://[server-host]:[server-port]" path="/server/storage/download/single/:type[dir,file]/:user/:root" method="get" summary="Download Single File" %}
{% swagger-description %}
 단일 파일 다운로드

\


디렉토리일 경우 압축을 한 다음 zip파일 형태로 다운받는다.
{% endswagger-description %}

{% swagger-parameter in="path" name="type" type="string" %}
file or dir
{% endswagger-parameter %}

{% swagger-parameter in="path" name="user" type="string" %}
target user
{% endswagger-parameter %}

{% swagger-parameter in="path" name="root" type="string" %}
target root
{% endswagger-parameter %}

{% swagger-parameter in="header" name="Set-Cookie" type="string" %}
token
{% endswagger-parameter %}

{% swagger-response status="200" description="return file information (+ raw data)" %}
```
{File information}
```
{% endswagger-response %}
{% endswagger %}

{% swagger baseUrl="http(s)://[server-host]:[server-port]" path="/server/storage/download/multiple/:user/:parentRoot:Files" method="get" summary="Download Multiple File" %}
{% swagger-description %}
 다중 파일 다운로드
{% endswagger-description %}

{% swagger-parameter in="path" name="user" type="string" %}
target user
{% endswagger-parameter %}

{% swagger-parameter in="header" name="Set-Cookie" type="string" %}
token
{% endswagger-parameter %}

{% swagger-parameter in="query" name="parentRoot" type="object" %}
list of file/directory root
{% endswagger-parameter %}

{% swagger-response status="200" description="return zip file" %}
```
{Zip file}
```
{% endswagger-response %}
{% endswagger %}

{% hint style="warning" %}
parentRoot는 쿼리 파라미터입니다. 그런데 다중 파일을 받게 되므로 해당 key format은 다음과 같습니다. 

file-1, file-2, dir-1, dir-2 ..
{% endhint %}

