from django.db import models
from django.conf import settings

class HasAuthorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(author__isnull=False)


class Post(models.Model):
    objects = HasAuthorManager()

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    photo = models.ImageField(upload_to='post')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class PostComment(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
