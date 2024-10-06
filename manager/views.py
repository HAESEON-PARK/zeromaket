
from django.shortcuts import render, get_object_or_404, redirect
from .models import Wholesalers
from .forms import WholesalerCreateForm  # 이 폼을 만들어야 합니다.

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
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'manager/edit_user.html', {'form': form})

# User 사용자 삭제 기능 (Delete)
def delete_user(request, user_id):
    user = get_object_or_404(Users, pk=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request, 'manager/delete_user.html', {'user': user})





# Wholesalers 모델 CRUD 구현

# Wholesaler 리스트 보기
def wholesaler_list(request):
    wholesalers = Wholesalers.objects.all()
    return render(request, 'manager/wholesaler_list.html', {'wholesalers': wholesalers})

# Wholesaler 생성하기
def wholesaler_create(request):
    if request.method == 'POST':
        form = WholesalerCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('wholesaler_list')
    else:
        form = WholesalerCreateForm()
    return render(request, 'manager/wholesaler_create.html', {'form': form})

# Wholesaler 상세보기
def wholesaler_detail(request, pk):
    wholesaler = get_object_or_404(Wholesalers, pk=pk)
    return render(request, 'manager/wholesaler_detail.html', {'wholesaler': wholesaler})

# Wholesaler 수정하기
def wholesaler_update(request, pk):
    wholesaler = get_object_or_404(Wholesalers, pk=pk)
    if request.method == 'POST':
        form = WholesalerCreateForm(request.POST, instance=wholesaler)
        if form.is_valid():
            form.save()
            return redirect('wholesaler_list')
    else:
        form = WholesalerCreateForm(instance=wholesaler)
    return render(request, 'manager/wholesaler_update.html', {'form': form, 'wholesaler': wholesaler})

# Wholesaler 삭제하기
def wholesaler_delete(request, pk):
    wholesaler = get_object_or_404(Wholesalers, pk=pk)
    if request.method == 'POST':
        wholesaler.delete()
        return redirect('wholesaler_list')
    return render(request, 'manager/wholesaler_delete.html', {'wholesaler': wholesaler})
