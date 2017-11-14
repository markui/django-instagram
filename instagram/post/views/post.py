"""
post_list뷰를 'post/' URL에 할당
"""
# from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
import json
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from ..models import Post, PostComment
from ..forms import PostForm, PostCommentForm
from ..decorators import login_required

__all__ = (
    'post_list',
    'post_detail',
    'post_create',
    'post_delete',
    'post_like',
)

def post_list(request):
    """
    모든 Post목록을 리턴
    template은 'post/post_list.html'을 사용
    :param request:
    :return:
    """
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'post/post_list.html', context)


def post_detail(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)

    comment_form = PostCommentForm()
    context = {
        'post': post,
    }
    return render(request, 'post/post_detail.html', context)

@login_required
def post_create(request):
    """
    HTTP GET: Post를 생성하는 빈 form을 보여주기
    HTTP POST: Post 생성하기

    1. 이 뷰에 접근할 때 해당 사용자가 인증된 상태가 아니면 로그인 뷰로 redirect
    2. form.is_valid()를 통과한 후 생성하는 Post객체에 author 정보를 추가하기
    :param request:
    :return:
    """
    # if not request.user.is_authenticated:
    #     return redirect('member:login')

    if request.method == "POST":
        # POST 요청의 경우 PostForm 인스턴스 생성과정에서 request.POST, request.FILES를 사용
        form = PostForm(request.POST, request.FILES)
        # form 생성과정에서 전달된 데이터들이 Form의 모든 field들에 유효한지 검사
        if form.is_valid():
            # 유효할 경우 Post인스턴스 생성 및 저장
            # 1. 커스텀 메서드 사용
            # form.save(author=request.user)

            # 2. 기존 Django의 ModelForm방식 사용
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post:list')
        # form의 field가 하나라도 유효하지 않은 경우
        else:
            print('Form is invalid!')

    # GET 요청에선 이부분이 무조건 실행
    # POST요청에선 form.is_valid()를통과하지 못하면 이부분이 실행
    else:
        form = PostForm()

    context = {
        'form': form
    }
    return render(request, 'post/post_form.html', context)


def post_delete(request, pk):
    """
    HTTP POST: Post 삭제하기
    :param request:
    :return:
    """
    # if not request.user.is_authenticated:
    #     return redirect('post:list')

    if request.method == "POST":
        post = get_object_or_404(Post, pk=pk)
        if post.author == request.user:
            post.delete()
            next = request.GET.get('next', '').strip()
            if next:
                return redirect(next)
        else:
            raise PermissionDenied('작성자가 아닙니다')


@login_required
def post_like(request):
    # user = request.user
    # if not user.is_authenticated:
    #     return HttpResponse(status=403)

    if request.method == "POST":
        user = request.user
        pk = request.POST.get('pk')
        post = get_object_or_404(Post, pk=pk)
        # 만약 user가 like 하지 않은 post라면, like 하기
        if not user.has_liked_post(post):
            user.like_post(post)
        # 만약 user가 이미 like 한 post라면, like 취소
        else:
            user.dislike_post(post)

        context = {
            'like_count': post.total_likes
        }
        return HttpResponse(json.dumps(context), content_type="application/json")

