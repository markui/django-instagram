from pprint import pprint
from typing import NamedTuple

import requests
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
#  from django.contrib.auth.models import User
# login view와 겹치므로 django_login으로 import하기
from django.contrib.auth import (
    get_user_model,
    authenticate,
    login as django_login,
    logout as django_logout,
)
from django.urls import reverse

from .forms import UserForm, LoginForm

User = get_user_model()


def signup(request):
    """
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.signup()



    else:
        form = UserForm()
    context = {
        "form": form
    }
    return render(request, 'member/signup.html' ,context)
    :param request:
    :return:
    """
    if request.method == "POST":
        # form에 데이터 바인딩
        form = UserForm(request.POST)
        # User.objects.filter(username=username).exists()
        if form.is_valid():
            # user = form.signup()
            user = form.save()
            # 회원가입이 완료된 후 해당 유저를 login 시킴
            django_login(request, user)
            return redirect('post:list')

    else:
        form = UserForm()
    context = {
        'form': form
    }
    return render(request, 'member/signup.html', context)


def login(request):
    next_path = request.GET.get('next')
    # POST요청(form submit)의 경우
    if request.method == 'POST':
        # form에 data binding
        form = LoginForm(request.POST)
        if form.is_valid():
            form.login(request)
            if next_path:
                return redirect(next_path)
        else:
            return HttpResponse('Login credentials invalid')
    else:
        form = LoginForm()
        facebook_app_id = settings.FACEBOOK_APP_ID
        facebook_scope = settings.FACEBOOK_SCOPE
        context = {
            'form': form,
            'facebook_app_id': facebook_app_id,
            'facebook_scope': facebook_scope
        }
        return render(request, 'member/login.html', context)

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


def logout(request):
    django_logout(request)
    return redirect('post:list')


def facebook_login(request):
    class AccessTokenInfo(NamedTuple):
        access_token: str
        token_type: str
        expires_in: str

    class DebugTokenInfo(NamedTuple):
        app_id: str
        application: str
        expires_at: int
        is_valid: bool
        issued_at: int
        scopes: list
        type: str
        user_id: str

    app_id = settings.FACEBOOK_APP_ID
    app_secret_code = settings.FACEBOOK_APP_SECRET_CODE
    app_access_token = f'{app_id}|{app_secret_code}'
    code = request.GET.get('code')

    def get_access_token_info(code_value):
        # 사용자가 페이스북에 로그인하기 위한 링크에 있던 'redirect_uri' GET파라미터의 값과 동일한 값
        redirect_uri = '{scheme}://{host}{relative_url}'.format(
            scheme=request.scheme,
            host=request.META['HTTP_HOST'],
            relative_url=reverse('member:facebook_login'),
        )
        print('redirect_uri:', redirect_uri)
        # 액세스 토큰을 요청하기 위한 엔드포인트
        url_access_token = 'https://graph.facebook.com/v2.10/oauth/access_token'
        # 액세스 토큰 요청의 GET파라미터 목록
        params_access_token = {
            'client_id': app_id,
            'redirect_uri': redirect_uri,
            'client_secret': app_secret_code,
            'code': code_value,
        }
        # 요청 후 결과를 받아옴
        response = requests.get(url_access_token, params_access_token)
        # 결과는 JSON형식의 텍스트이므로 아래와 같이 사용
        # json.loads(response.content) 와 같음

        # AccessTokenInfo(access_token=response.json()['access_token'],
        #    'token_type'=response.json()['token_type.....
        return AccessTokenInfo(**response.json())

    def get_debug_token_info(token):
        url_debug_token = 'https://graph.facebook.com/debug_token'
        params_debug_token = {
            'input_token': token,
            'access_token': app_access_token,
        }
        response = requests.get(url_debug_token, params_debug_token)
        return DebugTokenInfo(**response.json()['data'])

    # 전달받은 code값으로 AccessTokenInfo namedtuple을 반환
    access_token_info = get_access_token_info(code)
    # namedtuple에서 'access_token'속성의 값을 가져옴
    access_token = access_token_info.access_token
    # DebugTokenInfo 가져오기
    debug_token_info = get_debug_token_info(access_token)
    print(debug_token_info)

    # 유저 정보 가져오기
    user_info_fields = [
        'id',
        'name',
        'picture',
        # 'email',
    ]

    url_graph_user_info = 'https://graph.facebook.com/me'
    params_graph_user_info = {
        'fields': ','.join(user_info_fields),
        'access_token': access_token,
    }
    response = requests.get(url_graph_user_info, params_graph_user_info)
    result = response.json()
    return HttpResponse(result.items())
