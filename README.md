# django-blog
A blog web application built using the Django web framework
It has the following features:
* Basic authentication (register, login, logoutl Uses the built-in django.contrib.auth.User model)
* Create new posts (only registered users can do this and each post is linked the creator as the author(post.author)); each post has a title and a body. Uses a Post model)
* Edit and delete posts (this can only be done by the author of the post)
* Make comments on posts (only logged in users can do this. It employs a Comment model (with a commenter, associated post and date and time of the comment))

###### Hosted on Heroku: https://zuridjango-blog.herokuapp.com/
