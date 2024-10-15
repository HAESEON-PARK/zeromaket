from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login
from .forms import UserCreateForm, WholesalerForm, BuyerForm, CustomerForm, TotalProductsForm
from .models import Users, Wholesaler, Buyer, Customer, TotalProducts


def index(request):
    return render(request, 'management/index.html')  # 'index.html' 템플릿으로 렌더링

def user_list(request):
    users = Users.objects.all()  # 모든 사용자를 가져옵니다
    return render(request, 'management/user_list.html', {'users': users})  # 사용자 목록을 렌더링합니다.

# 사용자 추가 (Create)
def add_user(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')  # 사용자 목록 페이지로 리디렉션
    else:
        form = UserCreateForm()
    return render(request, 'management/add_user.html', {'form': form})

# 사용자 수정 (Update)
def edit_user(request, user_id):
    user = get_object_or_404(Users, pk=user_id)
    if request.method == 'POST':
        form = UserCreateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')  # 사용자 목록 페이지로 리디렉션
    else:
        form = UserCreateForm(instance=user)
    return render(request, 'management/edit_user.html', {'form': form})

def delete_user(request, user_id):
    user = get_object_or_404(Users, pk=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')  # 사용자 목록 페이지로 리디렉션
    return render(request, 'management/delete_user.html', {'user': user})

# 사용자 관리 (Admin)
def user_admin(request):
    users = Users.objects.all()  # 모든 사용자 가져오기
    return render(request, 'management/user_admin.html', {'users': users})

# Wholesaler 목록 보기 (Read)
def wholesaler_list(request):
    wholesalers = Wholesaler.objects.all()  # 모든 Wholesaler 가져오기
    return render(request, 'management/wholesaler_list.html', {'wholesalers': wholesalers})


# Wholesaler 생성하기 (Create)
@login_required
def wholesaler_create(request):
    if request.method == 'POST':
        form = WholesalerForm(request.POST, request.FILES)
        if form.is_valid():
            wholesaler = form.save(commit=False)
            wholesaler.user = request.user
            wholesaler.approve_status = 'pending'
            wholesaler.save()
            return redirect('wholesaler_await')  # 승인 대기 페이지로 리디렉션
    else:
        form = WholesalerForm()
    return render(request, 'management/wholesaler_form.html', {'form': form})

# Wholesaler 수정하기 (Update)
@login_required
def wholesaler_update(request, pk):
    wholesaler = get_object_or_404(Wholesaler, pk=pk, user=request.user)
    if request.method == 'POST':
        form = WholesalerForm(request.POST, request.FILES, instance=wholesaler)
        if form.is_valid():
            form.save()
            return redirect('wholesaler_list')  # 도매업자 목록 페이지로 리디렉션
    else:
        form = WholesalerForm(instance=wholesaler)
    return render(request, 'management/wholesaler_form.html', {'form': form})

# Wholesaler 삭제하기 (Delete)
@login_required
def wholesaler_delete(request, pk):
    wholesaler = get_object_or_404(Wholesaler, pk=pk, user=request.user)
    if request.method == 'POST':
        wholesaler.delete()
        return redirect('wholesaler_list')  # 도매업자 목록 페이지로 리디렉션
    return render(request, 'management/wholesaler_confirm_delete.html', {'wholesaler': wholesaler})

# Wholesaler 관리 (Admin)
def wholesaler_admin(request):
    wholesalers = Wholesaler.objects.all()  # 모든 도매업자 가져오기
    return render(request, 'management/wholesaler_admin.html', {'wholesalers': wholesalers})


@staff_member_required
def approve_wholesaler(request, pk):
    wholesaler = get_object_or_404(Wholesaler, pk=pk)
    wholesaler.approve_status = 'approved'
    wholesaler.save()
    # 승인 알림 등을 추가할 수 있습니다.
    return redirect('wholesaler_admin')

@staff_member_required
def reject_wholesaler(request, pk):
    wholesaler = get_object_or_404(Wholesaler, pk=pk)
    wholesaler.approve_status = 'rejected'
    wholesaler.save()
    # 거절 알림 등을 추가할 수 있습니다.
    return redirect('wholesaler_admin')




# Buyer 목록 보기 (Read)
def buyer_list(request):
    buyers = Buyer.objects.all()  # 모든 Buyer 가져오기
    return render(request, 'management/buyer_list.html', {'buyers': buyers})


# Buyer 생성하기 (Create)
def buyer_create(request):
    if request.method == 'POST':
        form = BuyerForm(request.POST, request.FILES)
        if form.is_valid():
            buyer = form.save(commit=False)
            buyer.user = request.user
            buyer.approve_status = 'pending'
            buyer.save()
            return redirect('buyer_await')  # 승인 대기 페이지로 리디렉션
    else:
        form = BuyerForm()
    return render(request, 'management/buyer_form.html', {'form': form})

# Buyer 수정하기 (Update)
@login_required
def buyer_update(request, pk):
    buyer = get_object_or_404(Buyer, pk=pk, user=request.user)
    if request.method == 'POST':
        form = BuyerForm(request.POST, request.FILES, instance=buyer)
        if form.is_valid():
            form.save()
            return redirect('buyer_list')  # 구매자 목록 페이지로 리디렉션
    else:
        form = BuyerForm(instance=buyer)
    return render(request, 'management/buyer_form.html', {'form': form})


# Buyer 삭제하기 (Delete)
@login_required
def buyer_delete(request, pk):
    buyer = get_object_or_404(Buyer, pk=pk, user=request.user)
    if request.method == 'POST':
        buyer.delete()
        return redirect('buyer_list')  # 구매자 목록 페이지로 리디렉션
    return render(request, 'management/buyer_confirm_delete.html', {'buyer': buyer})


# Buyer 관리 (Admin)
def buyer_admin(request):
    buyers = Buyer.objects.all()  # 모든 구매자 가져오기
    return render(request, 'management/buyer_admin.html', {'buyers': buyers})


@staff_member_required
def approve_buyer(request, pk):
    buyer = get_object_or_404(Buyer, pk=pk)
    buyer.approve_status = 'approved'
    buyer.save()
    # 승인 알림 등을 추가할 수 있습니다.
    return redirect('biyer_admin')

@staff_member_required
def reject_buyer(request, pk):
    buyer = get_object_or_404(buyer, pk=pk)
    buyer.approve_status = 'rejected'
    buyer.save()
    # 거절 알림 등을 추가할 수 있습니다.
    return redirect('buyer_admin')




# Customer 목록 보기 (Read)
def customer_list(request):
    customers = Customer.objects.all()  # 모든 고객 가져오기
    return render(request, 'management/customer_list.html', {'customers': customers})


# Customer 상세 보기 (Detail)
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, 'management/customer_detail.html', {'customer': customer})


# Customer 생성하기 (Create)
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')  # 고객 목록 페이지로 리디렉션
    else:
        form = CustomerForm()
    return render(request, 'managementr/customer_form.html', {'form': form})


# Customer 수정하기 (Update)
def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_detail', pk=pk)  # 수정 후 고객 상세 페이지로 리디렉션
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'management/customer_form.html', {'form': form})


# Customer 삭제하기 (Delete)
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('customer_list')  # 고객 목록 페이지로 리디렉션
    return render(request, 'management/customer_confirm_delete.html', {'customer': customer})


# Customer 관리 (Admin)
def customer_admin(request):
    customers = Customer.objects.all()  # 모든 고객 가져오기
    return render(request, 'management/customer_admin.html', {'customers': customers})


# 제품 관리 (Admin)
def product_admin(request):
    products = TotalProducts.objects.all()  # 모든 제품 가져오기
    return render(request, 'management/product_admin.html', {'products': products})




# 홈 페이지 뷰 (Home)
def home(request):
    return render(request, 'management/home.html')  # 홈 페이지 템플릿 렌더링




# 사용자 등록 뷰
def register(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.job_wholesaler and user.job_buyer:
                # 둘 다 선택한 경우 선택 페이지로 이동
                return redirect('select_business_form')
            elif user.job_wholesaler:
                return redirect('wholesaler_form')
            elif user.job_buyer:
                return redirect('buyer_form')
            else:
                # job type이 없으면 customer로 간주
                return redirect('customer_form')
    else:
        form = UserCreateForm()
    return render(request, 'register.html', {'form': form})

# Wholesaler 가입 폼 뷰
def wholesaler_form(request):
    if request.method == 'POST':
        form = WholesalerForm(request.POST, request.FILES, instance=request.user.wholesaler)
        if form.is_valid():
            wholesaler = form.save()
            # 승인 대기 페이지로 이동
            return redirect('wholesaler_await')
    else:
        form = WholesalerForm(instance=request.user.wholesaler)
    return render(request, 'wholesaler_form.html', {'form': form})

@login_required
def buyer_form(request):
    if request.method == 'POST':
        form = BuyerForm(request.POST, request.FILES, instance=request.user.buyer)
        if form.is_valid():
            buyer = form.save()
            # 승인 대기 페이지로 이동
            return redirect('buyer_await')
    else:
        form = BuyerForm(instance=request.user.buyer)
    return render(request, 'buyer_form.html', {'form': form})

# Customer 정보 입력 뷰
@login_required
def customer_form(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=request.user.customer)
        if form.is_valid():
            form.save()
            return redirect('customer_dashboard')  # 고객 대시보드로 리디렉션
    else:
        form = CustomerForm(instance=request.user.customer)
    return render(request, 'customer_form.html', {'form': form})


# TotalProducts CRUD 뷰
def product_list(request):
    products = TotalProducts.objects.all()
    return render(request, 'product_list.html', {'products': products})

# 제품 생성하기 (Create)
def product_create(request):
    if not request.user.is_staff:
        return redirect('home')  # 권한이 없는 경우 홈으로 리디렉션
    if request.method == 'POST':
        form = TotalProductsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = TotalProductsForm()
    return render(request, 'product_form.html', {'form': form})

# 제품 수정하기 (Update)
def product_update(request, pk):
    product = get_object_or_404(TotalProducts, pk=pk)
    if request.method == 'POST':
        form = TotalProductsForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = TotalProductsForm(instance=product)
    return render(request, 'product_form.html', {'form': form})

# 제품 삭제하기 (Delete)
def product_delete(request, pk):
    product = get_object_or_404(TotalProducts, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'product_confirm_delete.html', {'product': product})

