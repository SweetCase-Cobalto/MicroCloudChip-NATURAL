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
from django.urls import path, re_path

from app.views.user import *
from app.views.user_control_view import UserControlView
from app.views.data_control_view import DataControlView


urlpatterns = [
    path('admin/', admin.site.urls),

    path(r'server/user/login', view_user_login),
    path(r'server/user/logout', view_user_logout),
    path(r'server/user', view_add_user),
    path(r'server/user/<str:static_id>', UserControlView.as_view()),
    path('server/storage/data/<str:data_type>/<str:static_id>/<slug:root>', DataControlView.as_view())

]
