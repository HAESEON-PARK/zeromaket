# manager/views.py
from django.shortcuts import render

def index(request):
    return render(request, 'manager/index.html')


# manager/views.py
from django.shortcuts import render
from .models import Users

def user_list(request):
    users = Users.objects.all()
    return render(request, 'manager/user_list.html', {'users': users})


# views.py
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
