from django import forms
# from django.contrib.auth.models import User
from django.http import HttpResponse

from .validators import validate_username
from django.contrib.auth import get_user_model, authenticate, login as django_login

User = get_user_model()


class UserForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(),
        validators=[validate_username]
    )

    password = forms.CharField(
        widget=forms.PasswordInput(),
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(),
    )
    def clean_username(self):
        data = self.cleaned_data['username']
        if User.objects.filter(username=data).exists():
            raise forms.ValidationError('The username is already taken!')
        return data

    def clean_password2(self):
        """
        password, password2의 값이 같은지 비교
        다르면 raise forms.ValidationError
        :return:
        """
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError("The two passwords are not in sync")
        return password

    def clean(self):
        if self.is_valid():
            setattr(self, 'signup', self._signup)
        return self.cleaned_data


    def _signup(self):
        """
        User를 생성
        :return:
        """
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
        )
        print(f'{user.username} : {user.password}')

        # class Meta:
        #     model = User
        #     fields = [
        #         'username',
        #         'password',
        #     ]

        # def clean_username(self):
        #     data = self.cleaned_data['username']
        #     if User.objects.filter(username=data).exists():
        #         raise forms.ValidationError('The username is taken!')
        #     return data


class LoginForm(forms.Form):
    # 1. LoginForm을 만들고 username, password를 받을 수 있도록 구성
    # 2. def clean() 메서드에서 username, password를 사용해서
    #    authenticate에 성공했는지 실패했는지를 판단 실패시 raise forms.ValidationError
    # 3. LoginForm에 login(self, request) 메서드를 추가,
    #    이 메서드는 인수로 request객체를 받으며 호출시 django.contrib.auth.login() 메서드를 호출

    # username, password를 사용한 인증 관련 검증
    """
    is_valid()에서 주어진 username
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        # user를 나중에도 사용하기 위해서 __init__을 함
        # login에서 바로 self.user를 호출했을 때, 그 이전에 clean()이 호출되지 않았다면 참조 오류가 나기 때문이다

    username = forms.CharField(
        widget=forms.TextInput()
    )
    password = forms.CharField(
        widget=forms.PasswordInput()
    )

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        self.user = authenticate(
            username=cleaned_data.get('username'),
            password=cleaned_data.get('password'),
        )
        if not self.user:
            raise forms.ValidationError('Invalid user credentials')
        else:
            setattr(self, 'login', self._login)
            # 동적으로 속성 지정하고 싶을 때 setattr 사용
            # self.login = self._login

    def _login(self, request):
        """
        django.contrib.auth.login(request)를 실행
        :param request: django.contrib.auth.login()에 주어질 HttpRequest 객체
        :return:
        """
        # Django의 Session에 해당 User정보를 추가,
        # Response에는 SessionKey값을 Set-Cookie 헤더에 담아 보냄
        # 이후 브라우저와의 요청응답에서는 로그인을 유지함.
        django_login(request, self.user)
        # if self.user:
        #     django_login(request, self.user)
