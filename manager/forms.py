# forms.py
from django import forms
from .models import Users
from .models import Wholesaler
from .models import TotalProducts
from .models import Buyer

# User 사용자 추가 폼 정의
class UserCreateForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['email', 'name', 'phone', 'job', 'affiliation_type', 'affiliation_id']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '이메일'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '이름'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '전화번호'}),
            'job': forms.Select(attrs={'class': 'form-control'}),
            'affiliation_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '소속 타입'}),
            'affiliation_id': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '소속 ID'}),
        }
        labels = {
            'email': '이메일',
            'name': '이름',
            'phone': '전화번호',
            'job': '직무',
            'affiliation_type': '소속 타입',
            'affiliation_id': '소속 ID',
        }

# Wholesaler 추가 폼 정의
class WholesalerForm(forms.ModelForm):
    class Meta:
        model = Wholesaler
        fields = ['user', 'company_name', 'company_phone', 'company_address', 'business_registration_number', 'business_registration_certificate', 'bank_account', 'reliability_score']


# totalproducts CRUD 제어 폼 정의
class TotalProductsForm(forms.ModelForm):
    class Meta:
        model = TotalProducts
        fields = ['name', 'price', 'stock', 'description']



class BuyerForm(forms.ModelForm):
    class Meta:
        model = Buyer
        fields = ['user', 'company_name', 'company_phone', 'company_address', 'email', 'kakao_id', 'services', 'business_registration_number', 'business_registration_certificate', 'bank_account', 'manager_name', 'manager_phone', 'purchase_products', 'status', 'approve_status']


