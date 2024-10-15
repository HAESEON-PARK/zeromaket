# models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.conf import settings

# ENUM 타입 정의
USER_JOB_TYPE_CHOICES = [
    ('Wholesaler', 'Wholesaler'),
    ('buyer', 'Buyer'),
    ('customer', 'Customer'),
    ('manager', 'Manager'),
]

AFFILIATION_STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('on', 'On'),
    ('off', 'Off'),
]

MANAGER_ROLE_CHOICES = [
    ('internal_manager', 'Internal Manager'),
    ('delivery_manager', 'Delivery Manager'),
]

PAYMENT_STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('completed', 'Completed'),
]

DELIVERY_STATUS_CHOICES = [
    ('preparing', 'Preparing'),
    ('in_transit', 'In Transit'),
    ('delivered', 'Delivered'),
    ('rejected', 'Rejected'),
]

MANAGER_STATUS_CHOICES = [
    ('on', 'On'),
    ('off', 'Off'),
    ('rest', 'Rest'),
]

BUSINESS_STATUS_CHOICES = [
    ('open', 'Open'),
    ('close', 'Close'),
    ('rest', 'Rest'),
    ('closed_days', 'Closed Days'),
]

BUSINESS_APPROVE_STATUS_CHOICES = [
    ('approve', 'Approve'),
    ('reject', 'Reject'),
    ('hold', 'Hold'),
]

PRODUCT_STATUS_CHOICES = [
    ('new', 'New'),
    ('updated', 'Updated'),
]

SALE_STATUS_CHOICES = [
    ('new', 'New'),
    ('updated', 'Updated'),
]

VALIDATION_STATUS_CHOICES = [
    ('Valid', 'Valid'),
    ('Invalid', 'Invalid'),
]

SYNC_STATUS_CHOICES = [
    ('Success', 'Success'),
    ('Failure', 'Failure'),
]

# 모델 정의
class UserJobType(models.Model):
    job_name = models.CharField(max_length=50, unique=True, choices=USER_JOB_TYPE_CHOICES)

    def __str__(self):
        return self.job_name

# 커스텀 유저    
class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError('이메일 주소는 필수입니다.')
        if not name:
            raise ValueError('이름은 필수입니다.')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('슈퍼유저는 is_staff=True 이어야 합니다.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('슈퍼유저는 is_superuser=True 이어야 합니다.')
        return self.create_user(email, name, password, **extra_fields)



class Users(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=255)
    name = models.CharField(unique=True, max_length=100)
    phone = models.CharField(unique=True, max_length=20, null=True, blank=True)
    job_wholesaler = models.BooleanField(default=False)
    job_buyer = models.BooleanField(default=False)
    affiliation_type = models.CharField(max_length=50, null=True, blank=True)
    affiliation_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        creating = self.pk is None
        super().save(*args, **kwargs)  # 먼저 Users 인스턴스를 저장합니다.

        # Customer 프로필 생성 또는 업데이트
        customer, created = Customer.objects.get_or_create(user=self)
        customer.name = self.name
        customer.phone = self.phone
        customer.email = self.email
        customer.save()

        # Wholesaler 프로필 생성 또는 삭제
        if self.job_wholesaler:
            wholesaler, created = Wholesaler.objects.get_or_create(user=self)
            if created:
                wholesaler.approve_status = 'pending'
                wholesaler.status = 'close'  # 초기 상태 설정
                wholesaler.company_name = self.name  # 기본값 설정
                wholesaler.save()
        else:
            Wholesaler.objects.filter(user=self).delete()

        # Buyer 프로필 생성 또는 삭제
        if self.job_buyer:
            buyer, created = Buyer.objects.get_or_create(user=self)
            if created:
                buyer.approve_status = 'pending'
                buyer.status = 'close'  # 초기 상태 설정
                buyer.company_name = self.name  # 기본값 설정
                buyer.save()
        else:
            Buyer.objects.filter(user=self).delete()



class Wholesaler(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name='wholesaler')
    company_name = models.CharField(max_length=255, unique=True)
    company_phone = models.CharField(max_length=20, null=True, blank=True)
    company_address = models.CharField(max_length=255, null=True, blank=True)
    business_registration_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    business_registration_certificate = models.FileField(upload_to='certificates/', null=True, blank=True)
    bank_account = models.CharField(max_length=100, null=True, blank=True)
    manager_name = models.CharField(max_length=100, null=True, blank=True)
    manager_phone = models.CharField(max_length=20, null=True, blank=True)
    area = models.CharField(max_length=255, null=True, blank=True)
    reliability_score = models.IntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # 상태 필드 추가
    status = models.CharField(
        max_length=50,
        choices=BUSINESS_STATUS_CHOICES,
        default='close'
    )  # 상태

    # 승인 상태 필드 추가
    approve_status = models.CharField(
        max_length=50,
        choices=BUSINESS_APPROVE_STATUS_CHOICES,
        default='pending'
    )  # 승인 상태

    def __str__(self):
        return self.company_name




class TotalProducts(models.Model):
    product_code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.JSONField(null=True, blank=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    origin = models.CharField(max_length=100, null=True, blank=True)
    manufacturer = models.CharField(max_length=100, null=True, blank=True)
    barcode = models.CharField(max_length=13, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProductCodes(models.Model):
    total_product = models.ForeignKey('TotalProducts', on_delete=models.CASCADE)
    barcode = models.CharField(max_length=13, null=True, blank=True)
    gtin = models.CharField(max_length=14, null=True, blank=True)
    gpc_code = models.CharField(max_length=20, null=True, blank=True)
    food_industry_code = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['barcode', 'gtin', 'gpc_code', 'food_industry_code'], name='unique_product_code_combination')
        ]

    def __str__(self):
        return f"Product Code {self.id}"

class Buyer(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name='buyer')
    company_name = models.CharField(max_length=255)
    company_phone = models.CharField(max_length=20, null=True, blank=True)
    company_address = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    kakao_id = models.CharField(max_length=100, null=True, blank=True)
    services = models.TextField(null=True, blank=True)
    business_registration_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    business_registration_certificate = models.FileField(upload_to='certificates/', null=True, blank=True)
    bank_account = models.CharField(max_length=100, null=True, blank=True)
    manager_name = models.CharField(max_length=100, null=True, blank=True)
    manager_phone = models.CharField(max_length=20, null=True, blank=True)
    area_possible = models.CharField(max_length=255, null=True, blank=True)
    purchase_products = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시간
    updated_at = models.DateTimeField(auto_now=True)  # 수정 시간

    # 상태 필드 추가
    status = models.CharField(
        max_length=50,
        choices=BUSINESS_STATUS_CHOICES,
        default='open'
    )  # 상태

    # 승인 상태 필드 추가
    approve_status = models.CharField(
        max_length=50,
        choices=BUSINESS_APPROVE_STATUS_CHOICES,
        default='pending'
    )  # 승인 상태

    def __str__(self):
        return self.company_name



class Customer(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name='customer')
    name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)  
    email = models.EmailField(max_length=255, null=True, blank=True)  
    kakao_id = models.CharField(max_length=100, null=True, blank=True)  
    address = models.CharField(max_length=255, null=True, blank=True)  
    cart_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'customer'

    def __str__(self):
        return self.name if self.name else 'Customer ' + str(self.id)

class Quotations(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    supplier = models.ForeignKey(Wholesaler, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    details = models.JSONField()
    status = models.CharField(max_length=50, choices=[
        ('received', 'Received'),
        ('selected', 'Selected'),
        ('purchase_request', 'Purchase Request'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    ], default='received')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Quotation {self.id}"


class ValidationLogs(models.Model):
    product_code = models.ForeignKey(ProductCodes, on_delete=models.CASCADE)
    validation_status = models.CharField(max_length=50, choices=VALIDATION_STATUS_CHOICES)
    validation_message = models.TextField()
    validated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ValidationLog {self.id}"


class SyncLogs(models.Model):
    sync_type = models.CharField(max_length=50)
    sync_status = models.CharField(max_length=50, choices=SYNC_STATUS_CHOICES)
    sync_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"SyncLog {self.id}"


class Products(models.Model):
    total_product = models.ForeignKey('TotalProducts', on_delete=models.CASCADE)
    wholesaler = models.ForeignKey('Wholesaler', on_delete=models.CASCADE)
    product_data = models.JSONField()
    update_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, choices=PRODUCT_STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['total_product', 'wholesaler'], name='unique_total_product_wholesaler')
        ]

    def __str__(self):
        return f"Product {self.id}"


class SaleProducts(models.Model):
    wholesaler = models.ForeignKey(Wholesaler, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    sale_status = models.CharField(max_length=50, choices=SALE_STATUS_CHOICES, default='new')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['wholesaler', 'product'], name='unique_wholesaler_product')
        ]

    def __str__(self):
        return f"SaleProduct {self.id}"


class SomeModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)