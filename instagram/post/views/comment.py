"""
post_list뷰를 'post/' URL에 할당
"""
# from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, get_object_or_404

from ..forms import PostCommentForm
from ..models import Post, PostComment


__all__ = (
    'post_comment_create',
    'post_comment_delete',
)


def post_comment_create(request, post_pk):
    """
    HTTP POST: PostComment 생성하기
    로그인한 유저만 요청 가능하도록 함
    작성하는 Comment에 author정보 추가

    :param request:
    :return:
    """
    if not request.user.is_authenticated:
        return redirect('member:login')

    post = get_object_or_404(Post, pk=post_pk)
    if request.method == "POST":
        form = PostCommentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.post = post
            instance.author = request.user
            instance.save()
            # GET parameter로 next 값이 전달되면
            # 다음에 갈 URL (next)가 빈 문자열이 아닌 경우
            next = request.GET.get('next', '').strip()
            print(next)
            if next:
                return redirect(next)

    return redirect('post:list')


def post_comment_delete(request, pk):
    """
    HTTP POST: PostCommet 삭제하기
    :param request:
    :return:
    """
    if request.method == "POST":
        comment = get_object_or_404(PostComment, pk=pk)
        if comment.author == request.user:
            comment.delete()
            next = request.GET.get('next', '').strip()
            if next:
                return redirect(next)
        else:
            raise PermissionDenied('작성자가 아닙니다')

    return redirect('post:list')
