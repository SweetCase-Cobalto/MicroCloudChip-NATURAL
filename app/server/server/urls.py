"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url

from app.views.shared_file import *
from app.views.shared_file_control_view import SharedFileControlView
from app.views.user import *
from app.views.user_control_view import UserControlView
from app.views.data_control_view import DataControlView, search_storage_datas
from app.views.downloaders import *

from django.views.generic import TemplateView

urlpatterns = [
    # Production Version에서만 사용
    #url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    #url(r'^(storage)|(accounts)|(settings)|(share)/', TemplateView.as_view(template_name='index.html'), name='index'),

    #path('admin/', admin.site.urls),

    # User 관리
    path(r'server/user', view_add_user),
    path(r'server/user/login', view_user_login),
    path(r'server/user/logout', view_user_logout),
    path(r'server/user/list', view_get_user_list),

    # User Image Icon Download
    path(r'server/user/download/icon/<str:static_id>', view_download_user_icon),

    # user control
    path(r'server/user/<str:static_id>', UserControlView.as_view()),

    # Storage Data 관리
    path(r'server/storage/data/<str:data_type>/<str:static_id>/<path:root>', DataControlView.as_view()),

    # Storage 검색
    path(r'server/storage/search/<str:search_type>/<str:regex>', search_storage_datas),
    
    # Storage Data 다운로드
    path(r'server/storage/download/single/<str:data_type>/<str:static_id>/<path:root>', view_download_single_object),
    path(r'server/storage/download/multiple/<str:static_id>/<path:parent_root>', view_download_multiple_object),

    # Shared System)
    path(r'server/storage/shared/file', view_share_file),
    path(r'server/storage/shared/file/share-id', view_get_shared_id),
    path(r'server/storage/shared/file/<str:shared_id>', SharedFileControlView.as_view())

]
