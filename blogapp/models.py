from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.

class Author(AbstractUser):
  pass

class Post(models.Model):
  title = models.CharField(max_length=200)
  author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
  body = models.TextField()
  date = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.title

  def get_absolute_url(self):
    return reverse('post_detail', args=[self.pk])

class Comment(models.Model):
  comment = models.TextField()
  commenter = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='comments')
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
  date = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"comment made by {self.commenter} for {self.post.title} on {self.date}"