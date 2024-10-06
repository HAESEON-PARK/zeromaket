
from django.shortcuts import render, get_object_or_404, redirect
from .models import Wholesaler
from .forms import WholesalerForm  # 이 폼을 만들어야 합니다.
from .models import TotalProducts
from .forms import TotalProductsForm
from .models import Buyer
from .forms import BuyerForm

# index View 함수 정의
def index(request):
    return render(request, 'manager/index.html')

def home(request):
    return render(request, 'manager/home.html') # 홈페이지 템플릿 렌더링


# User 사용자 목록 보기 (Read)
from django.shortcuts import render
from .models import Users

def user_list(request):
    users = Users.objects.all()
    return render(request, 'manager/user_list.html', {'users': users})


# User 사용자 생성(Create)
from django.shortcuts import render, redirect
from .forms import UserCreateForm

def add_user(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')  # 사용자 목록 페이지로 리디렉션
    else:
        form = UserCreateForm()
    return render(request, 'manager/add_user.html', {'form': form})


# User 사용자 수정 기능(Update)
from django.shortcuts import get_object_or_404

def edit_user(request, user_id):
    user = get_object_or_404(Users, pk=user_id)
    if request.method == 'POST':
        form = UserCreateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserCreateForm(instance=user)
    return render(request, 'manager/edit_user.html', {'form': form})

# User 사용자 삭제 기능 (Delete)
def delete_user(request, user_id):
    user = get_object_or_404(Users, pk=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request, 'manager/delete_user.html', {'user': user})





# Wholesaler 모델 CRUD 구현

# Wholesaler 목록 보기 (Read)
def wholesaler_list(request):
    wholesaler = Wholesaler.objects.all()  # 모든 도매업자를 가져옴
    return render(request, 'wholesaler_list.html', {'wholesaler': wholesaler})

# Wholesaler 생성하기 (Create)
def wholesaler_create(request):
    if request.method == 'POST':
        form = WholesalerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('wholesaler_list')
    else:
        form = WholesalerForm()
    return render(request, 'wholesaler_form.html', {'form': form})

# Wholesaler 수정하기 (Update)
def wholesaler_update(request, pk):
    wholesaler = get_object_or_404(Wholesaler, pk=pk)
    if request.method == 'POST':
        form = WholesalerForm(request.POST, instance=wholesaler)
        if form.is_valid():
            form.save()
            return redirect('wholesaler_list')
    else:
        form = WholesalerForm(instance=wholesaler)
    return render(request, 'wholesaler_form.html', {'form': form})

# Wholesaler 삭제하기 (Delete)
def wholesaler_delete(request, pk):
    wholesaler = get_object_or_404(Wholesaler, pk=pk)
    if request.method == 'POST':
        wholesaler.delete()
        return redirect('wholesaler_list')
    return render(request, 'wholesaler_confirm_delete.html', {'wholesaler': wholesaler})


# totalproducts CRUD
# 제품 목록 보기 (Read)
def product_list(request):
    products = TotalProducts.objects.all()  # 모든 제품을 가져옴
    return render(request, 'product_list.html', {'products': products})

# 제품 생성하기 (Create)
def product_create(request):
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


#CRUD 기능을 위한 Buyer 뷰 만들기
# 구매자 목록 보기 (Read)
def buyer_list(request):
    buyers = Buyer.objects.all()  # 모든 구매자를 가져옴
    return render(request, 'buyer_list.html', {'buyers': buyers})

# 구매자 생성하기 (Create)
def buyer_create(request):
    if request.method == 'POST':
        form = BuyerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('buyer_list')
    else:
        form = BuyerForm()
    return render(request, 'buyer_form.html', {'form': form})

# 구매자 수정하기 (Update)
def buyer_update(request, pk):
    buyer = get_object_or_404(Buyer, pk=pk)
    if request.method == 'POST':
        form = BuyerForm(request.POST, instance=buyer)
        if form.is_valid():
            form.save()
            return redirect('buyer_list')
    else:
        form = BuyerForm(instance=buyer)
    return render(request, 'buyer_form.html', {'form': form})

# 구매자 삭제하기 (Delete)
def buyer_delete(request, pk):
    buyer = get_object_or_404(Buyer, pk=pk)
    if request.method == 'POST':
        buyer.delete()
        return redirect('buyer_list')
    return render(request, 'buyer_confirm_delete.html', {'buyer': buyer})