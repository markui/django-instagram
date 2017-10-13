from django.db import models


# Create your models here.

class Post(models.Model):
    photo = models.ImageField(upload_to='photo')
    created_date = models.DateTimeField(auto_now_add=True)


class PostComment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
