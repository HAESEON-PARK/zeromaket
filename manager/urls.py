# manager/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='manager_index'),  # 기본 루트 URL을 manager 앱의 index 뷰에 연결
]



urlpatterns = [
    path('', views.index, name='manager_index'),
    path('users/', views.user_list, name='user_list'),  # 사용자 목록 URL 추가
]

# manager/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='manager_index'),
    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.user_create, name='user_create'),  # 사용자 추가 URL 정의
]
