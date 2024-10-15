# 4. urls.py - URL 라우팅 정의
from django.urls import path
from . import views

# Url 설정 및 패턴 정의
urlpatterns = [
    path('', views.index, name='management_index'),  # 기본 루트 URL을 management 앱의 index 뷰에 연결

    # 사용자 CRUD
    path('users/', views.user_list, name='user_list'),  # 사용자 목록 보기
    path('add_user/', views.add_user, name='add_user'),  # 사용자 추가
    path('users/edit/<int:user_id>/', views.edit_user, name='edit_user'),  # 사용자 수정
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),  # 사용자 삭제
    path('users/admin/', views.user_admin, name='user_admin'),  # 사용자 관리

    # Wholesaler 모델 CRUD
    path('wholesaler/', views.wholesaler_list, name='wholesaler_list'),  # Wholesaler 목록 보기
    path('wholesaler/create/', views.wholesaler_create, name='wholesaler_create'),  # Wholesaler 생성
    path('wholesaler/update/<int:pk>/', views.wholesaler_update, name='wholesaler_update'),  # Wholesaler 수정
    path('wholesaler/delete/<int:pk>/', views.wholesaler_delete, name='wholesaler_delete'),  # Wholesaler 삭제
    path('wholesaler/admin/', views.wholesaler_admin, name='wholesaler_admin'),  # Wholesaler 관리

    # Buyer 모델 CRUD
    path('buyer/', views.buyer_list, name='buyer_list'),  # Buyer 목록 보기
    path('buyer/create/', views.buyer_create, name='buyer_create'),  # Buyer 생성
    path('buyer/update/<int:pk>/', views.buyer_update, name='buyer_update'),  # Buyer 수정
    path('buyer/delete/<int:pk>/', views.buyer_delete, name='buyer_delete'),  # Buyer 삭제
    path('buyer/admin/', views.buyer_admin, name='buyer_admin'),  # Buyer 관리

    # Customer 모델 CRUD
    path('customers/', views.customer_list, name='customer_list'),  # Customer 목록 보기
    path('customers/<int:pk>/', views.customer_detail, name='customer_detail'),  # Customer 상세 보기
    path('customers/new/', views.customer_create, name='customer_create'),  # Customer 생성
    path('customers/<int:pk>/edit/', views.customer_update, name='customer_update'),  # Customer 수정
    path('customers/<int:pk>/delete/', views.customer_delete, name='customer_delete'),  # Customer 삭제
    path('customers/admin/', views.customer_admin, name='customer_admin'),  # Customer 관리

    # TotalProducts 모델 CRUD
    path('products/', views.product_list, name='product_list'),  # 제품 목록 보기
    path('products/new/', views.product_create, name='product_create'),  # 제품 생성
    path('products/<int:pk>/edit/', views.product_update, name='product_update'),  # 제품 수정
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),  # 제품 삭제
    path('products/admin/', views.product_admin, name='product_admin'),  # 제품 관리
]