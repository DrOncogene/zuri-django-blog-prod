from django import forms
from .models import Post, Author
from django.contrib.auth.forms import UserCreationForm

class CommentForm(forms.Form):
  comment = forms.CharField(widget=forms.Textarea)

class NewPostForm(forms.ModelForm):
  class Meta:
    model = Post
    fields = ['title', 'body']

class SignUpForm(UserCreationForm):
  class Meta:
    model = Author
    fields = ['username', 'email', 'first_name', 'last_name']