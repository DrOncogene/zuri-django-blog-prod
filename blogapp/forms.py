from django import forms
from .models import Post

class CommentForm(forms.Form):
  comment = forms.CharField(widget=forms.Textarea)

class NewPostForm(forms.ModelForm):
  class Meta:
    model = Post
    fields = ['title', 'body']
