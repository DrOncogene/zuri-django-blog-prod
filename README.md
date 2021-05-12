# django-blog
This is the deployed version. The local version is on the 'blog-local-version' branch of this repo
A blog web application built using the Django web framework
It has the following features:
* Basic authentication (register, login, logoutl Uses the built-in django.contrib.auth.User model)
* Create new posts (only registered users can do this and each post is linked the creator as the author(post.author)); each post has a title and a body. Uses a Post model)
* Edit and delete posts (this can only be done by the author of the post)
* Make comments on posts (only logged in users can do this. It employs a Comment model (with a commenter, associated post and date and time of the comment))
* Password reset: This uses a filebased email backend to save the composed email containing the password reset link to a log file from which the link is grabbed and displayed in a page where the user is redirected to. This view validates the email given by the user to make sure it belongs to the current user.

###### Hosted on Heroku: https://zuridjango-blog.herokuapp.com/
