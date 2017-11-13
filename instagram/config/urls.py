"""instagram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from member.apis import Login, Signup
from post.apis import PostList, PostDetail
from .views import index

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index, name='index'),
    url(r'^post/', include('post.urls')),
    url(r'^member/', include('member.urls')),

    url(r'^api/post/$', PostList.as_view(), name='api-post'),
    url(r'^api/post/(?P<pk>\d+)/$', PostDetail.as_view(), name='api-post-detail'),

    url(r'^api/member/login/$', Login.as_view(), name='api-login'),
    url(r'^api/member/signup/$', Signup.as_view(), name='api-signup'),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)
