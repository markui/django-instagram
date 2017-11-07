# PostList를 리턴하는 APIView를 만드세요
# 근데 APIView를 상속받도록
# get 요청만 응답

# url 모듈은 분리
#   기존 url들은 r'^'에 매칭
#   각 애플리케이션의 apis모듈 (ex: post.apis, member.apis)는
#       r'^api/'에 매칭되도록
#       각 애플리케이션의 urls모듈을 패키지화
#           기존 urls모듈에 있던 내용은 urls/views.py로 이동
#           apis에 있던 내용은 urls/apis.py에 작성
#
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post
from .serializers import PostSerializer


class PostList(APIView):
    # api/post/
    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
