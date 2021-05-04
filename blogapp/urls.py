from django.urls import path, include
from .views import BlogDetailView, BlogListView, PostUpdateView, PostCreateView, PostUpdateView, PostDeleteView, SignUpView, SigninView, SignoutView, ResetPasswordView
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


urlpatterns = [
  path('password_reset/', ResetPasswordView.as_view(), name='password_reset'),
  path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
    template_name='blogapp/registration/password_reset_confirm.html', 
    success_url=reverse_lazy('login')
    ), name='password_reset_confirm'),
  path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(
    template_name='blogapp/registration/password_reset_done.html',
    ), name='password_reset_done'),
  path('logout/', SignoutView.as_view(), name='logout'),
  path('login/', SigninView.as_view(), name='login'),
  path('register/', SignUpView.as_view(), name='sign_up'),
  path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
  path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_edit'),
  path('post/new/', PostCreateView.as_view(), name='post_new'),
  path('post/<int:pk>/', BlogDetailView.as_view(), name='post_detail'),
  path('', BlogListView.as_view(), name='home'),
]