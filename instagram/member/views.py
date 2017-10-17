from django.http import HttpResponse
from django.shortcuts import render, redirect
#  from django.contrib.auth.models import User
# login view와 겹치므로 django_login으로 import하기
from django.contrib.auth import get_user_model, authenticate, login as django_login  #
from .forms import UserForm, LoginForm

User = get_user_model()


def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        # User.objects.filter(username=username).exists()
        if form.is_valid():
            form.signup()

    else:
        form = UserForm()
    context = {
        'form': form
    }
    return render(request, 'member/signup.html', context)


def login(request):
    # POST요청(form submit)의 경우
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            form.login(request)
            return redirect('post:list')
        else:
            return HttpResponse('Login credentials invalid')
    else:
        return render(request, 'member/login.html')

        #     password = request.POST['password']
        #     username = request.POST['username']
        #     # 해당하는 User가 있는지 인증
        #     user = authenticate(
        #         username=username,
        #         password=password
        #     )
        #     # 인증에 성공하면 user변수에 User객체가 할당, 실패시 None return
        #     if user is not None:
        #         # Django의 Session에 해당 User정보를 추가,
        #         # Response에는 SessionKey값을 Set-Cookie 헤더에 담아 보냄
        #         # 이후 브라우저와의 요청응답에서는 로그인을 유지함
        #         django_login(request, user)
        #         return redirect('post:list')
        #     # 실패시 실패 메시지 출력
        #     else:
        #         return HttpResponse('Login credentials invalid')
        # # GET요청(form submit)의 경우
        # else:
        # return render(request, 'member/login.html')
