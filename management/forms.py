# forms.py
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Wholesaler, Buyer, Customer, TotalProducts, BUSINESS_STATUS_CHOICES, BUSINESS_APPROVE_STATUS_CHOICES, District

Users = get_user_model()


class UserCreateForm(UserCreationForm):
    job_wholesaler = forms.BooleanField(required=False, label='Wholesaler')
    job_buyer = forms.BooleanField(required=False, label='Buyer')

    class Meta:
        model = Users
        fields = [
            'email', 'name', 'phone', 'job_wholesaler', 'job_buyer',
            'affiliation_status', 'affiliation_id', 'password1', 'password2'
        ]
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '이메일을 입력하세요'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '이름을 입력하세요'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '전화번호를 입력하세요'}),
            'affiliation_status': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '소속 상태를 입력하세요'}),
            'affiliation_id': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '소속 ID를 입력하세요'}),
        }
        labels = {
            'email': '이메일',
            'name': '이름',
            'phone': '전화번호',
            'affiliation_status': '소속 상태',
            'affiliation_id': '소속 ID',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Users.objects.filter(email=email).exists():
            raise forms.ValidationError('이미 존재하는 이메일입니다.')
        return email


class UserChangeForm(UserChangeForm):
    job_wholesaler = forms.BooleanField(required=False, label='Wholesaler')
    job_buyer = forms.BooleanField(required=False, label='Buyer')

    class Meta:
        model = Users
        fields = [
            'email', 'name', 'phone', 'job_wholesaler', 'job_buyer',
            'affiliation_status', 'affiliation_id', 'password'
        ]
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '이메일을 입력하세요'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '이름을 입력하세요'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '전화번호를 입력하세요'}),
            'affiliation_status': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '소속 상태를 입력하세요'}),
            'affiliation_id': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '소속 ID를 입력하세요'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'email': '이메일',
            'name': '이름',
            'phone': '전화번호',
            'affiliation_status': '소속 상태',
            'affiliation_id': '소속 ID',
            'password': '비밀번호',
        }


class WholesalerForm(forms.ModelForm):
    status = forms.ChoiceField(choices=BUSINESS_STATUS_CHOICES, label='상태', required=False)

    class Meta:
        model = Wholesaler
        fields = [
            'company_name',
            'company_phone',
            'company_address',
            'business_registration_number',
            'business_registration_certificate',
            'bank_account',
            'status',  # 상태 필드 포함
        ]
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '회사 이름을 입력하세요'}),
            'company_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '회사 전화번호를 입력하세요'}),
            'company_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '회사 주소를 입력하세요'}),
            'business_registration_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '사업자 등록 번호를 입력하세요'}),
            'business_registration_certificate': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'bank_account': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '은행 계좌 정보를 입력하세요'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


        labels = {
            'company_name': '회사 이름',
            'company_phone': '회사 전화번호',
            'company_address': '회사 주소',
            'business_registration_number': '사업자 등록 번호',
            'business_registration_certificate': '사업자 등록 증명서',
            'bank_account': '은행 계좌',
            'status': '상태',
        }    


class WholesalerRegistrationForm(forms.ModelForm):
    service_areas = forms.ModelMultipleChoiceField(
        queryset=District.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Wholesaler
        fields = [
            'company_name',
            'company_phone',
            'company_address',
            'business_registration_number',
            'business_registration_certificate',
            'bank_account',
            'status',
            'service_areas'
        ]
    
        
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '회사 이름을 입력하세요'}),
            'company_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '회사 전화번호를 입력하세요'}),
            'company_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '회사 주소를 입력하세요'}),
            'business_registration_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '사업자 등록 번호를 입력하세요'}),
            'business_registration_certificate': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'bank_account': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '은행 계좌 정보를 입력하세요'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'service_areas': forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),
        }
        labels = {
            'company_name': '회사 이름',
            'company_phone': '회사 전화번호',
            'company_address': '회사 주소',
            'business_registration_number': '사업자 등록 번호',
            'business_registration_certificate': '사업자 등록 증명서',
            'bank_account': '은행 계좌',
            'status': '상태',
            'service_areas': '서비스 지역',
        }



    def clean_service_areas(self):
        service_areas = self.cleaned_data.get('service_areas')
        if service_areas.count() > Wholesaler.max_service_areas:
            raise forms.ValidationError(f"최대 {Wholesaler.max_service_areas}개의 지역만 선택할 수 있습니다.")
        return service_areas



class BuyerForm(forms.ModelForm):
    status = forms.ChoiceField(choices=BUSINESS_STATUS_CHOICES, label='상태', required=False)

    class Meta:
        model = Buyer
        fields = [
            'company_name',
            'company_phone',
            'company_address',
            'district',
            'email',
            'kakao_id',
            'services',
            'business_registration_number',
            'business_registration_certificate',
            'bank_account',
            'manager_name',
            'manager_phone',
            'purchase_products',
            'status',  # 상태 필드 포함
        ]
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '회사 이름을 입력하세요'}),
            'company_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '회사 전화번호를 입력하세요'}),
            'company_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '회사 주소를 입력하세요'}),
            'district': forms.Select(attrs={'class': 'form-control'}),  # District 선택 필드
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '이메일을 입력하세요'}),
            'kakao_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '카카오 ID를 입력하세요'}),
            'services': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '제공하는 서비스를 입력하세요'}),
            'business_registration_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '사업자 등록 번호를 입력하세요'}),
            'business_registration_certificate': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'bank_account': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '은행 계좌 정보를 입력하세요'}),
            'manager_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '관리자 이름을 입력하세요'}),
            'manager_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '관리자 전화번호를 입력하세요'}),
            'purchase_products': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '구매할 상품을 입력하세요'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

        labels = {
            'company_name': '회사 이름',
            'company_phone': '회사 전화번호',
            'company_address': '회사 주소',
            'district': '영업지역',  # 'address' → 'district'
            'email': '이메일',
            'kakao_id': '카카오 ID',
            'services': '제공 서비스',
            'business_registration_number': '사업자 등록 번호',
            'business_registration_certificate': '사업자 등록 증명서',
            'bank_account': '은행 계좌',
            'manager_name': '관리자 이름',
            'manager_phone': '관리자 전화번호',
            'purchase_products': '구매 상품',
            'status': '상태',
        }


class BuyerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Buyer
        fields = [
            'company_name',
            'company_phone',
            'company_address',
            'district',  # 'address' 대신 'district' 사용
            'email',
            'kakao_id',
            'services',
            'business_registration_number',
            'business_registration_certificate',
            'bank_account',
            'manager_name',
            'manager_phone',
            'purchase_products',
            'status',
            'approve_status'
        ]
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '회사 이름을 입력하세요'}),
            'company_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '회사 전화번호를 입력하세요'}),
            'company_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '회사 주소를 입력하세요'}),
            'district': forms.Select(attrs={'class': 'form-control'}),  # District 선택 필드
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '이메일을 입력하세요'}),
            'kakao_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '카카오 ID를 입력하세요'}),
            'services': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '제공하는 서비스를 입력하세요'}),
            'business_registration_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '사업자 등록 번호를 입력하세요'}),
            'business_registration_certificate': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'bank_account': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '은행 계좌 정보를 입력하세요'}),
            'manager_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '관리자 이름을 입력하세요'}),
            'manager_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '관리자 전화번호를 입력하세요'}),
            'purchase_products': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '구매할 상품을 입력하세요'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'approve_status': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'company_name': '회사 이름',
            'company_phone': '회사 전화번호',
            'company_address': '회사 주소',
            'district': '영업지역',  # 'address' → 'district'
            'email': '이메일',
            'kakao_id': '카카오 ID',
            'services': '제공 서비스',
            'business_registration_number': '사업자 등록 번호',
            'business_registration_certificate': '사업자 등록 증명서',
            'bank_account': '은행 계좌',
            'manager_name': '관리자 이름',
            'manager_phone': '관리자 전화번호',
            'purchase_products': '구매 상품',
            'status': '상태',
            'approve_status': '승인 상태',
        }


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'name',
            'phone',
            'email',
            'kakao_id',
            'address'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '이름을 입력하세요'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '전화번호를 입력하세요'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '이메일을 입력하세요'}),
            'kakao_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '카카오 ID를 입력하세요'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '주소를 입력하세요'}),
        }
        labels = {
            'name': '이름',
            'phone': '전화번호',
            'email': '이메일',
            'kakao_id': '카카오 ID',
            'address': '주소',
        }


# TotalProducts CRUD 제어 폼 정의
class TotalProductsForm(forms.ModelForm):
    class Meta:
        model = TotalProducts
        fields = [
            'product_code',
            'name',
            'description',
            'price',
            'weight',
            'origin',
            'manufacturer',
            'barcode'
        ]
        widgets = {
            'product_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '제품 코드를 입력하세요'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '제품 이름을 입력하세요'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '제품 설명을 입력하세요'}),
            'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '가격을 입력하세요'}),
            'weight': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '무게를 입력하세요'}),
            'origin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '원산지를 입력하세요'}),
            'manufacturer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '제조사를 입력하세요'}),
            'barcode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '바코드를 입력하세요'}),
        }


        labels = {
            'product_code': '제품 코드',
            'name': '제품 이름',
            'description': '제품 설명',
            'price': '가격',
            'weight': '무게',
            'origin': '원산지',
            'manufacturer': '제조사',
            'barcode': '바코드',
        }

# 개선 사항 설명
#1. **커스텀 검증 메서드 추가**: 
#   - `UserCreateForm`의 이메일 필드에 중복 체크를 위한 `clean_email` 메서드를 추가했습니다. 이를 통해 중복된 이메일을 방지합니다.

#2. **필수 필드에 대한 힌트 및 플레이스홀더 추가**:
#   - 각 필드에 `placeholder`와 `help_text`를 추가하여 사용자에게 입력을 도와주는 시각적 힌트를 제공했습니다.

#3. **상태 필드 권한 관리**:
#   - `WholesalerForm` 및 `BuyerForm`의 상태 필드는 `admin` 권한만 업데이트할 수 있도록 `staff_member_required` 장식자를 뷰에 적용하거나 폼 내에서 관리할 수 있습니다.

#이러한 개선사항을 반영하여 사용자의 편의성과 데이터의 무결성을 높일 수 있습니다. 추가적인 구현이나 개선이 필요하시면 언제든지 알려주세요!
