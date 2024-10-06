# index View 함수 정의
from django.shortcuts import render

def index(request):
    return render(request, 'manager/index.html')


# 사용자 목록 보기 (Read)
from django.shortcuts import render
from .models import Users

def user_list(request):
    users = Users.objects.all()
    return render(request, 'manager/user_list.html', {'users': users})


# 사용자 생성(Create)
from django.shortcuts import render, redirect
from .forms import UserCreateForm

def user_create(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')  # 사용자 목록 페이지로 리디렉션
    else:
        form = UserCreateForm()
    return render(request, 'manager/user_create.html', {'form': form})


# 사용자 수정 기능(Update)
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

# 사용자 삭제 기능 (Delete)
def delete_user(request, user_id):
    user = get_object_or_404(Users, pk=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request, 'manager/delete_user.html', {'user': user})
