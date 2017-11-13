from django.conf.urls import url

from .views import signup, login, logout, facebook_login

app_name = 'member'

urlpatterns = [
    url(r'^signup/$', signup, name='signup'),  # member/signup/
    url(r'^login/$', login, name='login'),  # member/login/
    url(r'^logout/$', logout, name='logout'),  # member/logout/
    url(r'^facebook-login/$', facebook_login, name='facebook_login'),  # member/facebook_login/
]
