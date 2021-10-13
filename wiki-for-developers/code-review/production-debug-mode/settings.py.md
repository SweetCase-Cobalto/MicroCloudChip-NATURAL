# settings.py

[전체 코드](https://github.com/SweetCase-Cobalto/microcloudchip-natural/blob/master/app/server/server/urls.py)

## Secret Key

```python
# SECURITY WARNING: keep the secret key used in production secret!
# 해당 어플리케이션은 사용작 직접 NAS에 설치하게 되므로 50자 랜덤으로 설정한다.
chars = ''.join([string.ascii_letters, string.digits, string.punctuation]).\
    replace('\'', '').replace('"', '').replace('\\', '')
SECRET_KEY = ''.join([random.SystemRandom().choice(chars) for i in range(50)])
```

Secret key는 DJango에서 보안과 관련된 기능을 수행하는 데 사용합니다(Session,  message, 암호화 서명 등) 일반 프로젝트라면 SECRET_KEY를 다른 곳에 분리해서 저장하고 이를 불러오는 작업을 거치지만 사용자가 직접 설치해야 하기 때문에 50자 랜덤으로 놓고 저장합니다. 다시 실행될 때마다 secret key는 변경됩니다.

{% hint style="warning" %}
그러나 아직 DJango의 보안 기능에 대한 지식이 아직 부족하기 때문에 만일을 대비해 차후 버전에서는 Secret key의 생성 및 저장 방식을 변경할 예정입니다.
{% endhint %}

## html File

 개발 단계에서는 ReactJS, DJango 따로 작동해서 진행하지만 Production 단계에서는 html 정적 파일을 사용해야 합니다. 다라서 Production 단계에서는 개발 단계와는 달리 css, js, html파일을 해당 위치에 옮기는 작업을 거쳐야 합니다. 이를 settings.py에서 진행합니다.

### Debug Mode

```python
DEBUG = True
# DEBUG = False
```

DJango의 Debug Mode를 설정합니다. True를 설정하면 개발할 때 코드를 저정하면 프레임워크가 Reload 됩니다.

### Template File Root

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'templates', 'static')
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

```

* line 4, 5: TEMPLATES의 DIRS는 html 파일의 위치를 나타냅니다. 개발 단계에서는 필요가 없으므로 비어있는 배열로 정의하지만, Production 단계에서는 반드시 지정해야 합니다.
* line 18: STATICFILES_DIRS: js, css 파일이 들어가 있는 파일의 위치입니다. 개발을 진행할 때는 주석처리합니다.
* line 21: STATIC_ROOT: 실제로 작동되는 static file(js, css)의 위치 입니다. staticfiles dirs와 기능이 같아 보이겠지만 python manage.py collectstatic 명령어를 이용해 static dirs에 있는 정적 파일들을 static root로 이동시킵니다. 개발을 진행할 때는 주석처리 합니다.

## Allowed  hosts

```python
# in Development
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
    '[::1]',
]
# In Production
ALLOWED_HOSTS = [
    config['system']['host'],
    "0.0.0.0",
    "[::1]"
]

```

* allowed hosts는 개발 진행 때는 임의로 ip를 선택해서 해도 되지만, Production 단계에서는 설치할 어플리케이션의 서버 위치 IP를 허용해야 외부에서도 접근이 가능합니다. config.json에서 데이터를 참조합니다. 자세한 정보는 [해당 링크에서 확인하세요](https://seokbong60.gitbook.io/microcloudchip-natural/v/v0.0.x/wiki-for-developers/system-information-and-structure#data-layer-datalabel-layer)

