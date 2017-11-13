import io
import os
from random import randint

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files import File
from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.test import APILiveServerTestCase

User = get_user_model()

# URL_API_POST_LIST_NAME = 'api-post'
# URL_API_POST_LIST = '/api/post/'
# # Request객체를 생성 ('/api/post/')
# url = reverse('api-post')
# factory = APIRequestFactory()
# request = factory.get('/api/post/')
#
# # PostList.as_view()로 생성한 뷰 함수를 'view' 변수에 할당
# view = PostList.as_view()
# # view함수에 request를 전달
# response = view(request)
# # 결과는 JSON데이터
# pprint(len(response.data))
from post.apis import PostList
from post.models import Post


class PostListViewTest(APILiveServerTestCase):
    URL_API_POST_LIST_NAME = 'api-post'
    URL_API_POST_LIST = '/api/post/'
    VIEW_CLASS = PostList

    @staticmethod
    def create_user(username='dummy'):
        return User.objects.create_user(username=username)

    @staticmethod
    def create_post(author=None):
        return Post.objects.create(author=author, photo=File(io.BytesIO()))

    # url 이름이 url이랑 잘 매치되는지 (reverse)
    def test_post_list_url_name_reverse(self):
        url = reverse(self.URL_API_POST_LIST_NAME)
        self.assertEqual(url, self.URL_API_POST_LIST)

    # url이 url 이름과 잘 매치되는지 (resolve) => 다른 기능들도 함(resolver) => class.as_view() 새로 생성하는 것
    def test_post_list_url_resolve_view_class(self):
        # /api/post/에 매칭되는 ResolverMatch 객체를 가져옴
        resolver_match = resolve(self.URL_API_POST_LIST)
        # ResolverMatch의 url_name이 'api-post'(self.URL_API_POST_LIST_NAME)인지 확인
        self.assertEqual(
            resolver_match.url_name,
            self.URL_API_POST_LIST_NAME)
        # ResolverMatch의 func이 PostList(self.VIEW_CLASS)인지 확인
        self.assertEqual(
            resolver_match.func.view_class,
            self.VIEW_CLASS)

    def test_get_post_list_author_exists(self):
        """
        PostList의 GET요청 (Post목록)에 대한 테스트
        임의의 개수만큼 author가 있는 Post를 생성하고 해당 개수만큼 Response가 돌아오는지 확인

        :return:
        """
        user = self.create_user()
        # 0이상 20이하의 임의의 숫자 지정
        num = randint(0, 20)
        # num개수만큼 Post 생성, author를 지정해줌
        for i in range(num):
            Post.objects.create(
                author=user,
                photo=File(io.BytesIO),
            )

        url = reverse(self.URL_API_POST_LIST_NAME)
        # post_list에 GET요청 (이 response는 APIView Response 객체)
        response = self.client.get(url)
        # status code가 200인지 확인
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # objects.count 결과가 num과 같은지 확인
        self.assertEqual(Post.objects.count(), num)
        # response로 돌아온 OrderdDict리스트의 길이가 num과 같은지 확인
        self.assertEqual(len(response.data), num)

        # response로 돌아온 객체들이 각각 pk, author, photo, created_at 키값을 가지고 있는지 확인
        for i in range(num):
            cur_post_data = response.data[i]
            self.assertIn('pk', cur_post_data)
            self.assertIn('author', cur_post_data)
            self.assertIn('photo', cur_post_data)
            self.assertIn('created_at', cur_post_data)

    def test_get_post_list_exclude_author_is_none(self):
        """
        author가 None인 Post가 PostList get요청에서 제외되는지 테스트
        :return:
        """
        user = self.create_user()
        num_author_none_posts = randint(1, 10)
        num_posts = randint(11, 20)
        for i in range(num_author_none_posts):
            self.create_post()
        for i in range(num_posts):
            self.create_post(author=user)
        response = self.client.get(self.URL_API_POST_LIST)
        # author가 없는 post개수는 response에 포함되지 않는지 확인
        self.assertEqual(len(response.data), num_posts)

    def test_create_post(self):
        """
        Post가 Create 되는지 확인 (author가 있다는 상태)
        :return:
        """
        # 1. 임의의 숫자만큼 Post Create하기
        # 2. status 201 created인지 확인하기
        # 3. DB에 그만큼의 Post가 Create되었는지 확인하기
        user = self.create_user()
        print(user)
        # client = APIClient()
        self.client.force_authenticate(user=user)
        path = os.path.join(settings.STATIC_DIR, 'test', 'test.png')
        with open(path, 'rb') as photo:
            data = {'photo': photo}
            response = self.client.post(self.URL_API_POST_LIST, data)
        # response 코드가 201인지 확인
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # 1개의 포스트가 생성되었는지 확인
        self.assertEqual(Post.objects.count(), 1)
        print(response.data['photo'].split('/')[-1])
        print(Post.objects.get(pk=1).__str__())
        self.assertEqual(response.data['photo'].split('/')[-1], Post.objects.get(pk=1).__str__())
