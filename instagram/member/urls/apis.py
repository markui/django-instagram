from django.conf.urls import url

from ..apis import Login, Signup, FacebookLogin

urlpatterns = [
    url(r'^login/$', Login.as_view(), name='login'),
    url(r'^signup/$', Signup.as_view(), name='signup'),
    url(r'^facebook-login/$', FacebookLogin.as_view(), name='facebook-login'),
]
