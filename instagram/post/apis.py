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
from rest_framework import generics, mixins, permissions
from rest_framework.response import Response

from member.serializers import UserSerializer
from utils.permissions import IsAuthorOrReadOnly
from .models import Post
from .serializers import PostSerializer


class PostList(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# Post Detail APIView 생성
# APIView를 사용

# GET, PUT, DELETE
# class PostDetail(APIView):
#     def get_object(self, pk):
#         try:
#             post = Post.objects.get(pk=pk)
#         except post.DoesNotExist:
#             raise Http404
#
#         return post
#
#     def get(self, request, pk, format=None):
#         post = self.get_object(pk)
#         serializer = PostSerializer(post)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         post = self.get_object(pk)
#         serializer = PostSerializer(post, data=request.data)
#         if serializer.is_valid():
#             serializer.save(author=request.user)
#             return Response(serializer.data)
#         return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         post = self.get_object(pk)
#         post.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#
class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        # permissions.IsAuthenticatedOrReadOnly,
        permissions.IsAuthenticated,
    )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetail(generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        IsAuthorOrReadOnly,
    )


class PostLikeToggle(generics.GenericAPIView):
    queryset = Post.objects.all()

    # self.get_object() <- GenericAPIView에 이미 구현되어 있음
    # lookup_url_kwarg = 'post_pk' => default는 pk임
    # url패턴에서 특정 Post instance를 가져오기 위한 그룹명
    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        # 이미 유저의 like_posts목록에 현재 post(instance)가 존재할 경우
        if user.like_posts.filter(pk=instance.pk):
            user.like_posts.remove(instance)
            like_status = False
        else:
            user.like_posts.add(instance)
            like_status = True
        data = {
            'user': UserSerializer(user).data,
            'post': PostSerializer(instance).data,
            'result': like_status,
        }
        return Response(data)
