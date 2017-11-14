from django.conf.urls import url

from ..views.auth import signup, login, logout
from ..views.auth_facebook import facebook_login, FrontFacebookLogin

app_name = 'member'

urlpatterns = [
    url(r'^signup/$', signup, name='signup'),  # member/signup/
    url(r'^login/$', login, name='login'),  # member/login/
    url(r'^logout/$', logout, name='logout'),  # member/logout/
    url(r'^facebook-login/$', facebook_login, name='facebook-login'),  # member/facebook-login/
    url(r'^front-facebook-login/$', FrontFacebookLogin.as_view(), name='front-facebook-login'),
    # member/front-facebook-login/
]
