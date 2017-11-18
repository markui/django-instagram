from typing import NamedTuple

import requests
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer, SignupSerializer

User = get_user_model()


class Login(APIView):
    def post(self, request):
        # 전달받은 데이터: request.data를 사용
        # URL: /api/member/login/
        # 1. username/password를 받음
        # 2. authentication를 이용해 사용자 인증
        # 3. 인증된 사용자에 해당하는 토큰을 생성
        # 4. 사용자 정보와 token.key값을 Response로 준다
        print(request.data)
        username = request.data['username']
        password = request.data['password']
        print(password)
        # 전달받은 username, password값으로
        # authenticate실행
        user = authenticate(
            username=username,
            password=password
        )
        # user가 존재할 경우 ( authenticate 성공 )
        if user:
            # 'user'키에 다른 dict로 유저에 대한 모든 정보를 보내줌

            token, token_created = Token.objects.get_or_create(
                user=user,
            )
            serializer = UserSerializer(user)
            print(serializer.data)
            ret = {
                'token': token.key,
                'user': serializer.data,
            }
            return Response(ret, status=status.HTTP_200_OK)
        # 인증에 실패한 경우
        else:
            ret = {
                'message': 'Invalid credentials'
            }
            return Response(ret, status=status.HTTP_401_UNAUTHORIZED)


class Signup(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer

    # def post(self, request):
    #     # # 회원가입 후 토큰 생성 유저정보 및 토큰 키 반환
    #     # username = request.data['username']
    #     # password = request.data['password']
    #     #
    #     # if User.objects.filter(username=username).exists():
    #     #     return Response({'message': 'Username already exists'})
    #     # user = User.objects.create_user(
    #     #     username=username,
    #     #     password=password,
    #     # )
    #     # token = Token.objects.create(user=user)
    #     # data = {
    #     #     'user': UserSerializer(user).data,
    #     #     'token': token.key,
    #     # }
    #     # return Response(data)
    #
    #     serializer = SignupSerializer(data=request.data)
    #     if serializer.is_valid():
    #         user = serializer.save()
    #         data = {
    #             'user': serializer.data
    #         }
    #         return Response(data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # views.py에
    # class FrontFacebookLogin(View):
    # /member/front-facebook-login/
    # Facebook쪽 앱 설정에서 리다이렉트 URI에 위 URL을 추가

    # facebook_login() 뷰가 하던 일을 대부분 동일하게 하며 마지막 결과로
    # {'access_token': <액세스 토큰값>, 'facebook_user_id':
    # <해당유저의 app에 대한 페이스북 ID(고유값) }
    # 을 리턴하도록 함


# class FrontFacebookLogin(View):



class FacebookLogin(APIView):
    # /api/member/facebook-login/
    def post(self, request):
        # request.data에
        #   access_token
        #   facebook_user_id
        #       데이터가 전달됨

        # Debug결과의 NamedTuple
        class DebugTokenInfo(NamedTuple):
            app_id: str
            application: str
            expires_at: int
            is_valid: bool
            issued_at: int
            scopes: list
            type: str
            user_id: str

        # token(access_token)을 받아 해당 토큰을 Debug
        def get_debug_token_info(token):
            app_id = settings.FACEBOOK_APP_ID
            app_secret_code = settings.FACEBOOK_APP_SECRET_CODE
            app_access_token = f'{app_id}|{app_secret_code}'

            url_debug_token = 'https://graph.facebook.com/debug_token'
            params_debug_token = {
                'input_token': token,
                'access_token': app_access_token,
            }
            response = requests.get(url_debug_token, params_debug_token)
            return DebugTokenInfo(**response.json()['data'])

        # request.data로 전달된 access_token값을 페이스북API쪽에 debug요청, 결과를 받아옴
        debug_token_info = get_debug_token_info(request.data['access_token'])

        if debug_token_info.user_id != request.data['facebook_user_id']:
            raise APIException('페이스북 토큰의 사용자와 전달받은 facebook_user_id가 일치하지 않음')

        if not debug_token_info.is_valid:
            raise APIException('페이스북 토큰이 유효하지 않'
                               '음')

        # FacebookBackend를 사용해서 유저 인증
        user = authenticate(facebook_user_id=request.data['facebook_user_id'])
        # 인증에 실패한 경우 페이스북유저 타입으로 유저를 만들어줌
        print(user)
        if not user:
            user = User.objects.create_user(
                username=f'fb_{request.data["facebook_user_id"]}',
                user_type=User.USER_TYPE_FACEBOOK,
            )

        # 유저 시리얼라이즈 결과를 Response
        # token도 추가
        data = {
            'user': UserSerializer(user).data,
            'token': user.token,
        }
        return Response(data)
