"""
URL configuration for my_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
# 루트 url 추가하기
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from management import views  # management 앱의 views 파일에서 home 뷰를 가져옵니다.


urlpatterns = [
    path('admin/', admin.site.urls),
    path('management/', include('management.urls')),  # management 앱 URL 포함
    path('', views.home, name='home'),  # 루트 경로 추가
]
