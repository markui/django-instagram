from django.conf.urls import url, include
from django.contrib import admin

from ..views import index

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index, name='index'),
    url(r'^post/', include('post.urls.views', namespace='post')),
    url(r'^member/', include('member.urls.views', namespace='member')),
]
