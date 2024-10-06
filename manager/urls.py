# manager/urls.py
from django.urls import path
from . import views

#Url 설청, 패턴정의
urlpatterns = [
    path('', views.index, name='manager_index'),  # 기본 루트 URL을 manager 앱의 index 뷰에 연결
]

#사용자 목록 보기 (Read)
urlpatterns = [
    path('', views.index, name='manager_index'),
    path('users/', views.user_list, name='user_list'),  # 사용자 목록 URL 추가
]


# 사용자 추가 기능 (Create)
urlpatterns = [
    path('', views.index, name='manager_index'),
    path('users/', views.user_list, name='user_list'),
    path('add_user/', views.add_user, name='add_user'),  # 사용자 추가 URL 정의
]

# 사용자 수정 기능 (Update)
urlpatterns = [
    path('', views.index, name='manager_index'),
    path('users/', views.user_list, name='user_list'),
    path('add_user/', views.add_user, name='add_user'),
    path('users/edit/<int:user_id>/', views.edit_user, name='edit_user'),  # 사용자 수정 URL
]

# 사용자 삭제 기능 (Delete)
urlpatterns = [
    path('', views.index, name='manager_index'),
    path('users/', views.user_list, name='user_list'),
    path('add_user/', views.add_user, name='add_user'),
    path('users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),  # 사용자 삭제 URL
]


# Wholesalers 모델 CRUD 구현
urlpatterns = [
    path('', views.index, name='manager_index'),
    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.add_user, name='add_user'),
    # Wholesaler 관련 URL
    path('wholesalers/', views.wholesaler_list, name='wholesaler_list'),
    path('wholesalers/create/', views.wholesaler_create, name='wholesaler_create'),
    path('wholesalers/<int:pk>/', views.wholesaler_detail, name='wholesaler_detail'),
    path('wholesalers/<int:pk>/update/', views.wholesaler_update, name='wholesaler_update'),
    path('wholesalers/<int:pk>/delete/', views.wholesaler_delete, name='wholesaler_delete'),
]

