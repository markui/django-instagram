from django.conf.urls import url

from .views import signup, login

app_name = 'member'

urlpatterns = [
    url(r'^signup/$', signup, name='signup'),  # member/signup/
    url(r'^login/$', login, name='login'),  # member/login/
]
