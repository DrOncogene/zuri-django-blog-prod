import os
import time

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.urls import reverse_lazy
from django.shortcuts import reverse, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.utils.decorators import method_decorator
from django.http import HttpResponse, HttpResponseRedirect
from .forms import CommentForm, NewPostForm, SignUpForm

from .models import  Post, Comment, Author
# Create your views here.

class PostListView(ListView):
  model = Post
  template_name = 'blogapp/home.html'

class PostDetailView(DetailView):
  model = Post
  template_name = 'blogapp/post/post_detail.html'
  form_class = CommentForm

  @method_decorator(login_required(login_url='login'))
  def post(self, request, *args, **kwargs):
    form = self.form_class(request.POST)
    if form.is_valid():
      commenter = request.user
      post = Post.objects.get(id=request.POST['post'])
      comment_from_user = request.POST['comment']
      comment = Comment(comment=comment_from_user,commenter=commenter,post=post)
      comment.save()
      return HttpResponseRedirect(reverse('post_detail', args=[post.id]))
    
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    form = self.form_class
    context['form'] = form
    return context

class PostCreateView(LoginRequiredMixin, CreateView):
  login_url = reverse_lazy('login')
  model = Post
  template_name = 'blogapp/post/post_new.html'
  form_class = NewPostForm

  def post(self, request, *args, **kwargs):
    form = self.form_class(request.POST)
    if form.is_valid():
      title = request.POST['title']
      author = request.user
      body = request.POST['body']
      post = Post(title=title, author=author, body=body)
      post.save()
      return HttpResponseRedirect(reverse('post_detail', args=[post.id]))

class PostUpdateView(UserPassesTestMixin, UpdateView):
  model = Post
  template_name = 'blogapp/post/post_edit.html'
  fields = ['title', 'body']

  def test_func(self):
    return Post.objects.get(id=self.kwargs['pk']) in self.request.user.posts.all()

class PostDeleteView(UserPassesTestMixin, DeleteView):
  
  model = Post
  template_name = 'blogapp/post/post_delete.html'
  success_url = reverse_lazy('home')

  def test_func(self):
    return Post.objects.get(id=self.kwargs['pk']) in self.request.user.posts.all()
  
class SignUpView(CreateView):
  model = Author
  success_url = reverse_lazy('login')
  template_name = 'blogapp/registration/register.html'
  form_class = SignUpForm

class SigninView(LoginView):
  template_name = 'blogapp/registration/login.html'
  success_url = reverse_lazy('home')

class SignoutView(LogoutView):
  redirect_field_name = 'home'
  template_name = 'blogapp/registration/logout.html'

class ResetPasswordView(PasswordResetView):
  template_name='blogapp/registration/password_reset.html'

  def post(self, request):
    for file in os.scandir('sent_emails'):
      os.remove(file)
      
    super().post(request)
    if request.user.is_authenticated:
      if request.user.email == request.POST['email']:
        last_saved_email = os.listdir('sent_emails')[-1]
        with open(f"sent_emails/{last_saved_email}") as sent_mail:
          reset_url = sent_mail.readlines()[-11].split(' ')[-1]
          
        for file in os.scandir('sent_emails'):
          os.remove(file)

        return render(request, 'blogapp/registration/password_reset.html', {
          'reset_sent': bool(request.POST['reset_sent']),
          'password_reset_url': reset_url,
          'email_valid': request.user.email == request.POST['email'],
          'form': self.form_class(request.POST)
        })
      else:
        return render(request, 'blogapp/registration/password_reset.html', {
          'reset_sent': bool(request.POST['reset_sent']),
          'email_valid': request.user.email == request.POST['email'],
          'form': self.form_class(request.POST)
        })
    else:
      try:
        last_saved_email = os.listdir('sent_emails')[-1]
        with open(f"sent_emails/{last_saved_email}") as sent_mail:
          reset_url = sent_mail.readlines()[-11].split(' ')[-1]
          
        for file in os.scandir('sent_emails'):
          os.remove(file)

        return render(request, 'blogapp/registration/password_reset.html', {
          'reset_sent': bool(request.POST['reset_sent']),
          'password_reset_url': reset_url,
          'email_valid': True,
          'email': request.POST['email'],
          'form': self.form_class(request.POST)
        })
      except IndexError:
        return render(request, 'blogapp/registration/password_reset.html', {
          'reset_sent': bool(request.POST['reset_sent']),
          'email_exist': False,
          'email': request.POST['email'],
          'form': self.form_class(request.POST)
        })
  