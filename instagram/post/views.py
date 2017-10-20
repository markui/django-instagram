"""
post_list뷰를 'post/' URL에 할당
"""

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .models import Post, PostComment
from .forms import PostForm, PostCommentForm


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


def post_create(request):
    """
    HTTP GET: Post를 생성하는 빈 form을 보여주기
    HTTP POST: Post 생성하기

    1. 이 뷰에 접근할 때 해당 사용자가 인증된 상태가 아니면 로그인 뷰로 redirect
    2. form.is_valid()를 통과한 후 생성하는 Post객체에 author 정보를 추가하기
    :param request:
    :return:
    """
    if not request.user.is_authenticated:
        return redirect('member:login')

    if request.method == "POST":
        # POST 요청의 경우 PostForm 인스턴스 생성과정에서 request.POST, request.FILES를 사용
        form = PostForm(request.POST, request.FILES)
        # form 생성과정에서 전달된 데이터들이 Form의 모든 field들에 유효한지 검사
        if form.is_valid():
            photo = form.cleaned_data.get('photo')
            Post.objects.create(
                author=request.user,
                photo=photo
            )
            return redirect('post:list')
        # form의 field가 하나라도 유효하지 않은 경우
        else:
            print('Form is invalid!')

    # GET 요청에선 이부분이 무조건 실행
    # POST요청에선 form.is_valid()를 통과하지 못하면 이부분이 실행
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
    if not request.user.is_authenticated:
        return redirect('post:list')

    if request.method == "POST":
        post = Post.objects.get(pk=pk)
        if request.user == post.author:
            post.delete()

    return redirect('post:list')


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
            next = request.GET.get('next')
            if next:
                return redirect(next)

    return redirect('post:list')


def post_comment_delete(request, pk):
    """
    HTTP POST: PostCommet 삭제하기
    :param request:
    :return:
    """
    if not request.user.is_authenticated:
        return redirect('post:list')

    if request.method == "POST":
        comment = PostComment.objects.get(pk=pk)
        if request.user == comment.author:
            comment.delete()

    return redirect('post:list')
