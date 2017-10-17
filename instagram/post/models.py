from django.db import models


class Post(models.Model):
    photo = models.ImageField(upload_to='post')
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_date']
class PostComment(models.Model):
    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
