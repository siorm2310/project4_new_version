from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.utils.timezone import now


class User(AbstractUser):
    follows = models.ManyToManyField(
        'self', related_name='followers', symmetrical=False, blank=True)

    def __str__(self):
        return self.username


class Post(models.Model):
    creator = models.ForeignKey(
        User, on_delete=CASCADE, related_name="creator")
    title = models.CharField(max_length=32)
    content = models.CharField(max_length=180)
    likes = models.ManyToManyField(User, related_name="likes", blank=True)
    time = models.DateTimeField(default=now())

    def get_num_of_likes(self):
        return self.likes.all().__len__()

    def __str__(self):
        return self.title
