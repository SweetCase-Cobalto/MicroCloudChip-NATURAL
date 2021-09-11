"""
Django settings for server project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import random
import string
from pathlib import Path
import json
import os

config = None
# Load Config File
try:
    with open('server/config.json', 'r') as f:
        config = json.load(f)
except Exception as e:
    print("Config data is not setting, please back to `bin` directory and run command `perl install.pl install` ")
    exit(0)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# 해당 어플리케이션은 사용작 직접 NAS에 설치하게 되므로 50자 랜덤으로 설정한다.
chars = ''.join([string.ascii_letters, string.digits, string.punctuation]).\
    replace('\'', '').replace('"', '').replace('\\', '')
SECRET_KEY = ''.join([random.SystemRandom().choice(chars) for i in range(50)])

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    #'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
    'corsheaders'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware'
]

ROOT_URLCONF = 'server.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        #'DIRS': [os.path.join(BASE_DIR, 'templates')],
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
"""
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'templates', 'static')
]
"""
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


WSGI_APPLICATION = 'server.wsgi.application'
# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = None
# 타입에 따라 다름
try:
    if config["database"]["rdbms"]["type"] == "sqlite":
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
    elif config["database"]["rdbms"]["type"] == "mysql":
        DATABASES = {
            'default': {
                'ENGINE': config["database"]["rdbms"]["engine"],
                'NAME': config["database"]["rdbms"]["name"],
                'USER': config["database"]["rdbms"]["user"],
                'PASSWORD': config["database"]["rdbms"]["password"],
                'HOST': config["database"]["rdbms"]["host"],
                'PORT': str(config["database"]["rdbms"]["port"])
            }
        }
except Exception as e:
    print(e)
    print("config data has illeagal data")
    print("please back to bin directory and run `perl install.pl install` again ")
    exit(0)

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
    '[::1]',
]
"""
ALLOWED_HOSTS = [
    config['system']['host'],
    "0.0.0.0",
    "[::1]"
]
"""

CORS_ALLOW_HEADERS = [
    'Set-Cookie'
]
