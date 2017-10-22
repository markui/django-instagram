from django.conf.urls import url

from .views import (
    post_list,
    post_detail,
    post_create,
    post_delete,
    post_comment_create,
    post_comment_delete,
    post_like,
)

app_name = 'post'

urlpatterns = [
    url(r'^$', post_list, name='list'),  # /post
    url(r'^(?P<post_pk>\d+)/$', post_detail, name='detail'),  # /post/1
    url(r'^create/$', post_create, name='create'),  # /post/create/
    url(r'^(?P<pk>\d+)/delete/$', post_delete, name='delete'),  # /post/1/delete
    url(r'^like/$', post_like, name='like'), # /post/like
    url(r'^(?P<post_pk>\d+)/comment/create/$', post_comment_create, name='comment_create'),  # /post/1/comment/create
    url(r'^(?P<pk>\d+)/comment/delete/$', post_comment_delete, name='comment_delete'),  # /post/1/comment/delete
]
