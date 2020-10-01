from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE


class User(AbstractUser):
    follows = models.ManyToManyField('self', related_name='followers', symmetrical=False, null=True,blank=True)

class Post(models.Model):
    creator = models.ForeignKey(User,on_delete=CASCADE)
    title = models.CharField(max_length=32)
    content = models.CharField(max_length=180)
    likes = models.IntegerField(default=0)
