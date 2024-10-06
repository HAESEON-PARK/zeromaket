# models.py
from django.db import models

# ENUM 타입 정의
USER_JOB_TYPE_CHOICES = [
    ('wholesaler', 'Wholesaler'),
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


class Users(models.Model):
    password = models.BinaryField()
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, unique=True)
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    job = models.ForeignKey(UserJobType, on_delete=models.SET_NULL, null=True, blank=True)
    affiliation_type = models.CharField(max_length=50, null=True, blank=True)
    affiliation_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Wholesalers(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    contact_info = models.JSONField()
    status = models.CharField(max_length=50, choices=BUSINESS_STATUS_CHOICES, default='open')
    approve_status = models.CharField(max_length=50, choices=BUSINESS_APPROVE_STATUS_CHOICES, default='hold')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


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
    total_product = models.ForeignKey(TotalProducts, on_delete=models.CASCADE)
    barcode = models.CharField(max_length=13, null=True, blank=True)
    gtin = models.CharField(max_length=14, null=True, blank=True)
    gpc_code = models.CharField(max_length=20, null=True, blank=True)
    food_industry_code = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('barcode', 'gtin', 'gpc_code', 'food_industry_code')


class Buyer(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    company_phone = models.CharField(max_length=20, null=True, blank=True)
    company_address = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    kakao_id = models.CharField(max_length=100, null=True, blank=True)
    services = models.TextField(null=True, blank=True)
    business_registration_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    business_registration_certificate = models.BinaryField(null=True, blank=True)
    bank_account = models.CharField(max_length=100, null=True, blank=True)
    manager_name = models.CharField(max_length=100, null=True, blank=True)
    manager_phone = models.CharField(max_length=20, null=True, blank=True)
    purchase_products = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=BUSINESS_STATUS_CHOICES, default='open')
    approve_status = models.CharField(max_length=50, choices=BUSINESS_APPROVE_STATUS_CHOICES, default='hold')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name


class Customer(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    kakao_id = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Quotations(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    supplier = models.ForeignKey(Wholesalers, on_delete=models.CASCADE)
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
    total_product = models.ForeignKey(TotalProducts, on_delete=models.CASCADE)
    wholesaler = models.ForeignKey(Wholesalers, on_delete=models.CASCADE)
    product_data = models.JSONField()
    update_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, choices=PRODUCT_STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('total_product', 'wholesaler')

    def __str__(self):
        return f"Product {self.id}"


class SaleProducts(models.Model):
    wholesaler = models.ForeignKey(Wholesalers, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    sale_status = models.CharField(max_length=50, choices=SALE_STATUS_CHOICES, default='new')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('wholesaler', 'product')

    def __str__(self):
        return f"SaleProduct {self.id}"
