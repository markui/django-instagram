from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
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
                'message': 'Invalide credentials'
            }
            return Response(ret, status=status.HTTP_401_UNAUTHORIZED)


class Signup(APIView):
    def post(self, request):
        # # 회원가입 후 토큰 생성 유저정보 및 토큰 키 반환
        # username = request.data['username']
        # password = request.data['password']
        #
        # if User.objects.filter(username=username).exists():
        #     return Response({'message': 'Username already exists'})
        # user = User.objects.create_user(
        #     username=username,
        #     password=password,
        # )
        # token = Token.objects.create(user=user)
        # data = {
        #     'user': UserSerializer(user).data,
        #     'token': token.key,
        # }
        # return Response(data)

        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            data = {
                'user': serializer.data
            }
            return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
