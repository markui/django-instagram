from django.conf.urls import url

from .views import signup, login, logout

app_name = 'member'

urlpatterns = [
    url(r'^signup/$', signup, name='signup'),  # member/signup/
    url(r'^login/$', login, name='login'),  # member/login/
    url(r'^logout/$', logout, name='logout'), # member/logout/
]
