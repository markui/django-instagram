from urllib.parse import urlparse

from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse


def login_required(view_func):
    def wrapped_view_func(*args, **kwargs):
        request = args[0]
        if not request.user.is_authenticated:
            # 기존: /member/login/
            # 변경: /member/login/?next=[HTTP_REFERER]
            referer = urlparse(request.META['HTTP_REFERER']).path
            url = '{base_url}?next={referer}'.format(
                base_url=reverse('member:login'),
                referer=referer)
            print(request.path)
            print(url)
            # return redirect(url)
            return HttpResponse(status=403)
        return view_func(*args, **kwargs)

    return wrapped_view_func
