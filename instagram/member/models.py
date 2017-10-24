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
    USER_TYPE_FACEBOOK = 'f'
    USER_TYPE_DJANGO = 'd'

    CHOICES_USER_TYPE = (
        (USER_TYPE_FACEBOOK, 'Facebook'),
        (USER_TYPE_DJANGO, 'Django'),
    )
    user_type = models.CharField(
        max_length=1,
        choices=CHOICES_USER_TYPE
    )
    # 내가 팔로우 하고 있는 유저 목록
    #
    # 내가 A를 follow한다
    #   나는 A의 follower
    #   A는 나의 followed_user이다

    # 나를 follow하고 있는 사람 목록은
    # followers
    # 내가 follow하고 있는 사람 목록은
    # followed_users

    following_users = models.ManyToManyField(
        'self',
        symmetrical=False,
        through='Relation',
        related_name='followers',
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

    def follow_toggle(self, user):
        # 1. 주어진 user가 User객체인지 확인
        #   아니면 raise ValueError()
        # 2. 주어진 user를 follow하고 있으면 해제
        #   안 하고 있으면 follow함
        if not isinstance(user, User):
            raise ValueError('"user" argument must be User instance!')
        relation, relation_created = self.following_user_relations.get_or_create(to_user=user)
        # 팔로우를 하지 않은 경우
        if relation_created:
            return True
        # 팔로우를 한 경우
        relation.delete()
        return False

        # REQUIRED_FIELDS = AbstractUser.REQUIRED_FIELDS + ['age']

    objects = UserManager()

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = f'{verbose_name} 목록'


class Relation(models.Model):
    from_user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='following_users_relation')
    to_user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='follower_relation')
    created_at = models.DateTimeField(auto_now_add=True)

    # relation_type -> choice field -> 차단/팔로우
    # 그러면, following -> 도 다 바꿔야함 뭐 from/to_users_relation처럼
    # 그런데 그냥 2개의 다른 모델 정의하는 것도 한 방법이다
    def __str__(self):
        return f'Relation (from: {self.from_user.username}, to: {self.to_user.username}'
