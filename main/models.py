from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    confirmation_email_sent = models.BooleanField(default=False)
    email_confirmed = models.BooleanField(default=False)
    confirmation_code = models.CharField(
        max_length=100, blank=True, null=True
    )


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
