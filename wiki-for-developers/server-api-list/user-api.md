---
description: User 관련 API
---

# User API

{% swagger baseUrl="http(s)://[server-host]:[server-port]" path="/server/user/login" method="post" summary="User Login" %}
{% swagger-description %}
 유저 로그인 API
{% endswagger-description %}

{% swagger-parameter in="body" name="pswd" type="string" %}
User Password
{% endswagger-parameter %}

{% swagger-parameter in="body" name="email" type="string" %}
User Email
{% endswagger-parameter %}

{% swagger-response status="200" description="Success Login" %}
```
{  
    "code": 0,
    "data": {
        "token": [JWT 복호화 키],
        "name": [user name],
        "static-id": [user static id],
        "email": [user email],
        "is-admin": [is user admin (boolean)],
        "volume-type" : {
            "name": [volue type name],
            "value": {
                "unit": [volume type: GB, TB etc..],
                "volume": [volume value],
            }
        }
    }
}
```
{% endswagger-response %}
{% endswagger %}

{% swagger baseUrl="http(s)://[server-host]:[server-port]" path="/server/user/logout" method="get" summary="User Logout" %}
{% swagger-description %}
User 로그아웃
{% endswagger-description %}

{% swagger-parameter in="header" name="Set-Cookie" type="string" %}
token
{% endswagger-parameter %}

{% swagger-response status="200" description="로그아웃 성공시 0, 실패시 0이 아닌 다른 코" %}
```
{ code: 0 }
```
{% endswagger-response %}
{% endswagger %}

{% swagger baseUrl="http(s)://[server-host]:[server-port]" path="/server/user" method="post" summary="Add User" %}
{% swagger-description %}
유저 생성
{% endswagger-description %}

{% swagger-parameter in="header" name="Set-Cookie" type="string" %}
token
{% endswagger-parameter %}

{% swagger-parameter in="body" name="img" type="object" %}
Image File Of User Icon(jpg, png, gif)
{% endswagger-parameter %}

{% swagger-parameter in="body" name="email" type="string" %}
User Email
{% endswagger-parameter %}

{% swagger-parameter in="body" name="password" type="string" %}
New User Password
{% endswagger-parameter %}

{% swagger-parameter in="body" name="volume-type" type="string" %}
Level Of User (사용할 수 있는 용량 타입) (Ex: TEST->1K)
{% endswagger-parameter %}

{% swagger-parameter in="body" name="name" type="string" %}
New User Name
{% endswagger-parameter %}

{% swagger-response status="200" description="If success then return 0 else over 0" %}
```
{
    "code": [integer]
}
```
{% endswagger-response %}
{% endswagger %}

{% swagger baseUrl="http(s)://[server-host]:[server-port]" path="/server/user/:userid" method="patch" summary="Modify User Info" %}
{% swagger-description %}
유저 정보 변경하기
{% endswagger-description %}

{% swagger-parameter in="path" name="userid" type="string" %}
taget user static-id
{% endswagger-parameter %}

{% swagger-parameter in="header" name="Set-Cookie" type="string" %}
token
{% endswagger-parameter %}

{% swagger-parameter in="body" name="img" type="object" %}
image object for change new user icon
{% endswagger-parameter %}

{% swagger-parameter in="body" name="password" type="string" %}
change by new password
{% endswagger-parameter %}

{% swagger-parameter in="body" name="name" type="string" %}
change by new name
{% endswagger-parameter %}

{% swagger-parameter in="body" name="image-changeable" type="integer" %}
if 0 then don't change image else change image
{% endswagger-parameter %}

{% swagger-response status="200" description="If success then return 0 else over 0" %}
```
{
    "code": [integer]
}
```
{% endswagger-response %}
{% endswagger %}

{% swagger baseUrl="http(s)://[server-host]:[server-port]" path="/server/user/:userid" method="delete" summary="Remove User" %}
{% swagger-description %}
 유저 삭제하기
{% endswagger-description %}

{% swagger-parameter in="path" name="userid" type="string" %}
target user static id
{% endswagger-parameter %}

{% swagger-parameter in="header" name="Set-Cookie" type="string" %}
token
{% endswagger-parameter %}

{% swagger-response status="200" description="If success return 0 else then over 0" %}
```
{ code: [integer] }
```
{% endswagger-response %}
{% endswagger %}

{% swagger baseUrl="http(s)://[server-host]:[server-port]" path="/server/user/:userid" method="get" summary="Get User Info" %}
{% swagger-description %}
유저 데이터 가지고 오기
{% endswagger-description %}

{% swagger-parameter in="path" name="userid" type="string" %}
target user static id
{% endswagger-parameter %}

{% swagger-parameter in="header" name="Set-Cookie" type="string" %}
token
{% endswagger-parameter %}

{% swagger-response status="200" description="If success then return 0 else return over Zero" %}
```
{
    code: [integer],
    user-info: {
        name: [user name],
        pswd: [user password],
        email: [user email],
        is-admin: [True or False],
        volume-type: [volume type(TEST, GUEST etc...)],
        static-id: [user id]
    }
    used-volume: {
        type: [volume type(KB, MB etc...)],
        value: [float]
    }   
}
```
{% endswagger-response %}
{% endswagger %}

{% swagger baseUrl="http(s)://[server-host]:[server-port]" path="/server/user/list" method="get" summary="Get User List" %}
{% swagger-description %}
  유저 리스트 갖고오기 (Admin 계정만 사용할 수 있음)
{% endswagger-description %}

{% swagger-parameter in="header" name="Set-Cookie" type="string" %}
token
{% endswagger-parameter %}

{% swagger-response status="200" description="if error then return 
{ code: error (0 > ) }
" %}
```
{    
    code: [integer],
    data: [
        {
            username: [user name],
            user_static_id: [user static id],
            userImgLink: [user image link],
            isAdmin: [is admin]
        }, {}, {}...
    ]
}
```
{% endswagger-response %}
{% endswagger %}

