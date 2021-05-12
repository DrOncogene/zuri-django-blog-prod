from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth import login

from blogapp.models import Author, Post, Comment

# Create your tests here.

class TestViewsClass(TestCase):

  # @classmethod
  # def setUpTestData(cls):
  #   cls.author = Author.objects.create_user(
  #     username='testUser', 
  #     password='125dhjdjhdyu855', 
  #     first_name='Rasheed', 
  #     last_name='Nasir', 
  #     email='kay@djangoblog.com'
  #   )
  #   cls.post = Post.objects.create(
  #     title='Test Post', 
  #     body='A test post', 
  #     author=cls.author
  #   )
  #   cls.comment = Comment.objects.create(
  #     comment='A test comment', 
  #     commenter=cls.author, 
  #     post=cls.post
  #   )
  #   print(Author.objects.get(id=1).comments)
  #   print(Post.objects.get(id=1).comments)
  #   cls.author.save()
  #   cls.post.save()
  #   comment.save()

  def setUp(self):
    self.author = Author.objects.create_user(
      username='testUser', 
      password='125dhjdjhdyu855', 
      first_name='User', 
      last_name='User', 
      email='kay@djangoblog.com'
    )
    self.post = Post.objects.create(
      title='Test Post', 
      body='A test post', 
      author=self.author
    )
    self.comment = Comment.objects.create(
      comment='A test comment', 
      commenter=self.author, 
      post=self.post
    )
    self.author.save()
    self.post.save()
    self.comment.save()

  def test_post_list_view(self):
    response = self.client.get(reverse('home'))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, 'Test Post')
    self.assertTemplateUsed(response, 'blogapp/home.html')
    
  def test_post_detail_view(self):
    response = self.client.get('/post/1/')
    no_response = self.client.get('/post/10/')
    self.assertEqual(response.status_code, 200)
    self.assertEquals(no_response.status_code, 404)
    self.assertContains(response, 'A test post')
    self.assertTemplateUsed(response, 'blogapp/post/post_detail.html')

  def test_comment_in_post_detail_view(self):
    login = self.client.login(username='testUser', password='125dhjdjhdyu855')
    response = self.client.post(
      '/post/1/', 
      {
        "comment": 'Another test comment', 
        "post": self.post.id,
      }
    )
    self.assertEqual(response.status_code, 302)
    self.assertEqual(Comment.objects.get(id=2).comment, 'Another test comment')

  def test_post_create_view(self):
    login = self.client.login(username='testUser', password='125dhjdjhdyu855')
    get_response = self.client.get(reverse('post_new'))
    post_response = self.client.post(
      reverse('post_new'), 
      {
        "title": 'Test Post 2', 
        "body": 'Test post two', 
        "author": get_response.context['user']
      }
    )
    self.assertEqual(get_response.status_code, 200)
    self.assertEqual(post_response.status_code, 302)
    self.assertContains(get_response, 'New Post')
    self.assertEqual(str(Post.objects.get(id=2)), 'Test Post 2')
    self.assertTemplateUsed(get_response, 'blogapp/post/post_new.html')

  def test_post_update_view(self):
    login = self.client.login(username='testUser', password='125dhjdjhdyu855')
    get_response = self.client.get('/post/1/update/')
    self.assertEqual(str(get_response.context['user']), 'testUser')
    post_response = self.client.post(
      reverse('post_edit', kwargs={"pk": self.post.id}), 
      {
        "title": 'Edited Title', 
        "body": 'Edited post body'
      }
    )
    self.assertEqual(get_response.status_code, 200)
    self.assertEqual(post_response.status_code, 302)
    self.post.refresh_from_db()
    self.assertEqual(self.post.title, 'Edited Title')
    self.assertContains(get_response, 'Edit Post')
    self.assertTemplateUsed(get_response, 'blogapp/post/post_edit.html')

  def test_post_delete_view(self):
    login = self.client.login(username='testUser', password='125dhjdjhdyu855')
    post_2 = Post.objects.create(title='Test Post 2', author=self.author, body='Second Test Post')
    post_2.save()
    self.assertEqual(str(Post.objects.get(id=2)), 'Test Post 2')
    self.assertEqual(len(Post.objects.all()), 2)
    response = self.client.post(reverse('post_delete', kwargs={"pk": post_2.id}))
    self.assertEqual(response.status_code, 302)
    self.assertEqual(len(Post.objects.all()), 1)