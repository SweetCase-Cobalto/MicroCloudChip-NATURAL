# urls.py

[전체 코드](https://github.com/SweetCase-Cobalto/microcloudchip-natural/blob/master/app/server/server/urls.py)

디버깅 모드와는 달리 배포 모드에서는 브라우저에서도 지원해야 하기 때문에 urlpattern에서 아래와 같은 url이 추가됩니다. 단 디버깅 모드에서는 위의 코드를 주석 처리해서 작업합니다.

```python
from django.views.generic import TemplateView

...

url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
url(r'^(storage)|(accounts)|(settings)/', TemplateView.as_view(template_name='index.html'), name='index'),
```

* 5 line: 브라우저를 통해 어플리케이션에 접근 할 경우 html 파일을 받아와야 하므로 index.html를 연결합니다.
* 6 line: 그러나 5 line만 작성하면 (http://\[host]:\[port])만 접속되고 (http:/\[host]:\[port]/....)에서는 html 파일을 찾을 수 없다는 에러가 발생합니다. 0.0.x 기준의 어플리케이션은 storage, acocunts, settings 세 가지의 컨텐츠가 있으므로 url를 추가합니다. 이렇게 되면 http://\[host]:\[port]/storage 또는 \~/accounts,  /settings에 접근할 수 있습니다.

{% hint style="info" %}
**???: 이렇게 해놓으면 백엔드 url과 겹치지 않을까요?**

백엔드 url은 맨 앞부분에 server를 붙습니다. 그렇기 때문에 겹칠 일이 없습니다.

```python
# User 관리
path(r'server/user', view_add_user),
path(r'server/user/login', view_user_login),
path(r'server/user/logout', view_user_logout),
path(r'server/user/list', view_get_user_list),
```
{% endhint %}
