from django.conf.urls import url

from ..views.comment import (

    post_comment_create,
    post_comment_delete,

)
from .. import views

app_name = 'post'

urlpatterns = [
    url(r'^$', views.post_list, name='list'),  # /post
    url(r'^(?P<post_pk>\d+)/$', views.post_detail, name='detail'),  # /post/1
    url(r'^create/$', views.post_create, name='create'),  # /post/create/
    url(r'^(?P<pk>\d+)/delete/$', views.post_delete, name='delete'),  # /post/1/delete
    url(r'^like/$', views.post_like, name='like'),  # /post/like
    url(r'^(?P<post_pk>\d+)/comment/create/$', views.post_comment_create, name='comment_create'),  # /post/1/comment/create
    url(r'^(?P<pk>\d+)/comment/delete/$', views.post_comment_delete, name='comment_delete'),  # /post/1/comment/delete
]
