from django.db import models
from django.shortcuts import reverse
# from django.contrib.auth.models import AbstractBaseUser

# Create your models here.

# class User(AbstractBaseUser):
#   # groups = models.
#   pass

class Post(models.Model):
  title = models.CharField(max_length=200)
  author = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='posts')
  body = models.TextField()

  def __str__(self):
    return self.title

  def get_absolute_url(self):
    return reverse('post_detail', args=[str(self.pk)])

class Comment(models.Model):
  comment = models.TextField(null=True)
  commenter = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name='comments')
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
  date = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"comment made by {self.commenter} for {self.post.title} on {self.date} "