from django.conf.urls import url

from ..apis import PostList, PostDetail, PostLikeToggle

urlpatterns = [
    url(r'^$', PostList.as_view(), name='post-list'),
    url(r'^(?P<pk>\d+)/$', PostDetail.as_view(), name='post-detail'),
    url(r'^(?P<pk>\d+)/like-toggle/$', PostLikeToggle.as_view(), name='post-like-toggle'),
]
