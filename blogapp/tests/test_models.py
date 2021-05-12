from django.test import TestCase

from ..models import Author, Post, Comment

# Create your tests here.

class TestModelsClass(TestCase):

  @classmethod
  def setUpTestData(cls):
    cls.author = Author.objects.create(
      username='kayode', 
      password='testpassword', 
      first_name='Rasheed', 
      last_name='Nasir', 
      email='kay@djangoblog.com'
    )
    cls.post = Post.objects.create(
      title='Test Post', 
      body='A test post', 
      author=cls.author
    )
    cls.comment = Comment.objects.create(
      comment='A test comment', 
      commenter=cls.author, 
      post=cls.post
    )

  def test_author_username_label(self):
    username_label = self.author._meta.get_field('username').verbose_name
    self.assertEqual(username_label, 'username')
  
  def test_author_first_name_label(self):
    first_name_label = self.author._meta.get_field('first_name').verbose_name
    self.assertEqual(first_name_label, 'first name')
  
  def test_author_last_name_label(self):
    last_name_label = self.author._meta.get_field('last_name').verbose_name
    self.assertEqual(last_name_label, 'last name')

  def test_author_password_label(self):
    password_label = self.author._meta.get_field('password').verbose_name
    self.assertEqual(password_label, 'password')

  def test_post_content(self):
    self.assertEqual(self.post.title, 'Test Post')
    self.assertEqual(self.post.body, 'A test post')
    self.assertEqual(self.post.author, self.author)

  def test_comment_content(self):
    self.assertEqual(self.comment.comment, 'A test comment')
    self.assertEqual(self.comment.commenter, self.author)
    self.assertEqual(self.comment.post, self.post)

  def test_post_string(self):
    self.assertEqual(str(self.post), self.post.title)

  def test_post_absolute_url(self):
    self.assertEqual(self.post.get_absolute_url(), f"/post/{self.post.pk}/")

  def test_comment_string(self):
    self.assertEqual(str(self.comment), f"comment made by {self.comment.commenter} for {self.comment.post} on {self.comment.date}")


  
  
  

  