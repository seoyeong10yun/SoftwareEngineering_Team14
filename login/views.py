from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User

# Create your views here.
def LoginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            #print("로그인 성공")
            return redirect('recommand:content_list')
        else:
            context = {
                'error' : 'invaild credentials',
            }
            #print("로그인 실패")
            return render(request, 'login/login.html', context=context)
    else:
        return render(request, 'login/login.html')

@login_required
def LogoutView(request):
    logout(request)
    #print("로그아웃 성공")
    return redirect('accounts:login')

def SignUpView(request):
    if request.method == 'POST':
        password1 = request.POST['password']
        password2 = request.POST['password_confirm']
        if password1 == password2:
            user = User.objects.create_user(
                username = request.POST['username'],
                password = password1,
            )
            login(request, user)
            return redirect('recommand:content_list')
        else:
            context = {
                'error' : 'Sign up Fail',
            }
            return render(request, 'login/signup.html', context=context)
    else:
        return render(request, 'login/signup.html')