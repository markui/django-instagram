from django.db import models

from django.contrib.auth.models import (
    AbstractUser,
    UserManager,
    # UserManager as DjangoUserManager
)

from post.models import Post


# class UserManager(DjangoUserManager):
#     def create_superuser(self, *args, **kwargs):
#         return super().create_superuser(age=30, *args, **kwargs)


class User(AbstractUser):
    img_profile = models.ImageField(
        '프로필 이미지',
        upload_to='user',
        blank=True)
    # age = models.IntegerField()

    like_posts = models.ManyToManyField(
        'post.Post',
        related_name='liked_users',
        verbose_name='좋아요 누른 포스트 목록'
    )

    # 포스트 좋아요를 하기
    def like_post(self, post):
        self.like_posts.add(post)

    # 포스트 좋아요를 취소하기
    def dislike_post(self, post):
        self.like_posts.remove(post)

    # 포스트 좋아요가 이미 되어 있는지를 검사하기
    def has_liked_post(self, post):
        return self.like_posts.filter(pk=post.pk).exists()

    objects = UserManager()

    # REQUIRED_FIELDS = AbstractUser.REQUIRED_FIELDS + ['age']
    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = f'{verbose_name} 목록'
