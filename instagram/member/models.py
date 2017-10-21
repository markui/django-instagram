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
        'post.Post',  # 바로 앱에서 갖고 올 수 있음
        related_name='liked_users',
        verbose_name='좋아요 누른 포스트 목록'
    )

    def like_post(self, post):
        self.like_posts.add(post)

    objects = UserManager()

    # REQUIRED_FIELDS = AbstractUser.REQUIRED_FIELDS + ['age']
    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = f'{verbose_name} 목록'
