# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .forms import UserCreateForm, UserChangeForm
from .models import Wholesaler, Buyer, Customer, ProductCodes, TotalProducts, Quotations, ValidationLogs, SyncLogs, Products, SaleProducts

Users = get_user_model()

# 사용자(AdminUser) 관리자 설정
@admin.register(Users)
class UsersAdmin(BaseUserAdmin):
    model = Users
    add_form = UserCreateForm
    form = UserChangeForm

    list_display = (
        'id', 'email', 'name', 'phone', 'job_wholesaler', 'job_buyer',
        'affiliation_type', 'affiliation_id',
        'is_staff', 'is_active', 'created_at', 'updated_at'
    )
    list_filter = ('is_staff', 'is_active', 'job_wholesaler', 'job_buyer', 'affiliation_type')
    search_fields = ('email', 'name', 'phone')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'phone', 'job_wholesaler', 'job_buyer', 'affiliation_type', 'affiliation_id')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'phone', 'job_wholesaler', 'job_buyer', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            # 새로운 사용자 추가 시 User 객체를 먼저 저장하여 pk 생성
            obj.save()

        if not obj.job_wholesaler and not obj.job_buyer:
            customer, created = Customer.objects.get_or_create(user=obj)
            if created:
                customer.name = obj.name
                customer.phone = obj.phone
                customer.email = obj.email
                customer.save()
        else:
            # job_wholesaler나 job_buyer가 선택된 경우 기존 customer 레코드가 있는지 확인하고 삭제
            Customer.objects.filter(user=obj).delete()

        # super() 호출 후에 obj를 저장하여 외래 키 문제가 발생하지 않도록 함
        super().save_model(request, obj, form, change)


# Wholesaler 관리자 설정
@admin.register(Wholesaler)
class WholesalerAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'company_name', 'company_phone',
        'company_address', 'business_registration_number',
        'bank_account', 'reliability_score',
        'status',         # 상태 필드 추가
        'approve_status', # 승인 상태 필드 추가
        'created_at', 'updated_at'
    )
    search_fields = ('company_name', 'business_registration_number', 'user__name')
    list_filter = ('status', 'approve_status', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    actions = ['approve_wholesalers', 'reject_wholesalers']

    def approve_wholesalers(self, request, queryset):
        queryset.update(approve_status='approved')
        self.message_user(request, "선택된 도매상을 승인하였습니다.")
    approve_wholesalers.short_description = "선택된 도매상을 승인합니다"

    def reject_wholesalers(self, request, queryset):
        queryset.update(approve_status='rejected')
        self.message_user(request, "선택된 도매상을 거절하였습니다.")
    reject_wholesalers.short_description = "선택된 도매상을 거절합니다"


# Buyer 관리자 설정
@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'company_name', 'company_phone',
        'company_address', 'email', 'kakao_id', 'services',
        'business_registration_number', 'bank_account',
        'manager_name', 'manager_phone', 'purchase_products',
        'status',         # 상태 필드 추가
        'approve_status', # 승인 상태 필드 추가
        'created_at', 'updated_at'
    )
    search_fields = ('company_name', 'business_registration_number', 'user__name')
    list_filter = ('status', 'approve_status', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    actions = ['approve_buyers', 'reject_buyers']

    def approve_buyers(self, request, queryset):
        queryset.update(approve_status='approved')
        self.message_user(request, "선택된 구매자를 승인하였습니다.")
    approve_buyers.short_description = "선택된 구매자를 승인합니다"

    def reject_buyers(self, request, queryset):
        queryset.update(approve_status='rejected')
        self.message_user(request, "선택된 구매자를 거절하였습니다.")
    reject_buyers.short_description = "선택된 구매자를 거절합니다"

## 개선된 점 설명

#1. **검색 필드 확장**:
#   - `WholesalerAdmin`과 `BuyerAdmin` 클래스의 `search_fields`에 사용자 이름(`user__name`)을 추가하여 더 구체적인 검색이 가능하도록 개선했습니다.

#2. **`readonly_fields`의 일관성 유지**:
#   - `created_at`, `updated_at`과 같은 시간 필드를 읽기 전용으로 설정하여 데이터 무결성을 유지하도록 하였습니다.

#3. **관리자 액션 추가**:
#   - 승인 및 거절을 위한 액션을 여러 모델에 일관되게 추가하였습니다. 이는 일괄 작업을 수행하는 데 매우 유용합니다.

#이와 같은 설정을 통해 Django 관리자 패널에서 모델 데이터를 보다 효과적으로 관리할 수 있으며, 사용자와 관련된 정보를 쉽게 검색하고 수정할 수 있습니다. 추가적인 도움이 필요하시면 언제든지 알려주세요!


# 4. Customer 관리자 설정
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'name', 'phone', 'email',
        'kakao_id', 'address', 'created_at', 'updated_at'
    )
    search_fields = ('name', 'email', 'phone')
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

# 5. TotalProducts 관리자 설정
@admin.register(TotalProducts)
class TotalProductsAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'product_code', 'name', 'description',
        'price', 'weight', 'origin', 'manufacturer',
        'barcode', 'created_at', 'updated_at'
    )
    search_fields = ('product_code', 'name', 'barcode')
    list_filter = ('origin', 'manufacturer', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

# 6. ProductCodes 관리자 설정
@admin.register(ProductCodes)
class ProductCodesAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'total_product', 'barcode', 'gtin',
        'gpc_code', 'food_industry_code',
        'created_at', 'updated_at'
    )
    search_fields = ('barcode', 'gtin', 'gpc_code', 'food_industry_code')
    list_filter = ('total_product', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

# 7. Quotations 관리자 설정
@admin.register(Quotations)
class QuotationsAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'buyer', 'customer', 'supplier',
        'total_amount', 'status', 'created_at', 'updated_at'
    )
    search_fields = ('buyer__company_name', 'customer__name', 'supplier__company_name')
    list_filter = ('status', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

# 8. ValidationLogs 관리자 설정
@admin.register(ValidationLogs)
class ValidationLogsAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'product_code', 'validation_status',
        'validation_message', 'validated_at'
    )
    search_fields = ('product_code__barcode', 'validation_status')
    list_filter = ('validation_status', 'validated_at')
    ordering = ('-validated_at',)
    readonly_fields = ('validated_at',)

# 9. SyncLogs 관리자 설정
@admin.register(SyncLogs)
class SyncLogsAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'sync_type', 'sync_status',
        'sync_message', 'created_at'
    )
    search_fields = ('sync_type', 'sync_status')
    list_filter = ('sync_status', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

# 10. Products 관리자 설정
@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'total_product', 'wholesaler',
        'status', 'created_at', 'updated_at'
    )
    search_fields = ('total_product__name', 'wholesaler__company_name')
    list_filter = ('status', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

# 11. SaleProducts 관리자 설정
@admin.register(SaleProducts)
class SaleProductsAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'wholesaler', 'product',
        'sale_status', 'updated_at'
    )
    search_fields = ('wholesaler__company_name', 'product__total_product__name')
    list_filter = ('sale_status', 'updated_at')
    ordering = ('-updated_at',)
    readonly_fields = ('updated_at',)
