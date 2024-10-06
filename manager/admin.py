# admin.py
from django.contrib import admin
from .models import (
    UserJobType, Users, Wholesaler, TotalProducts, ProductCodes,
    Buyer, Customer, Quotations, ValidationLogs, SyncLogs,
    Products, SaleProducts
)

# 모든 모델을 관리자 페이지에 등록
admin.site.register(UserJobType)
admin.site.register(Users)
admin.site.register(Wholesaler)
admin.site.register(TotalProducts)
admin.site.register(ProductCodes)
admin.site.register(Buyer)
admin.site.register(Customer)
admin.site.register(Quotations)
admin.site.register(ValidationLogs)
admin.site.register(SyncLogs)
admin.site.register(Products)
admin.site.register(SaleProducts)
