from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tweet(models.Model): 
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    body = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now=True)
    num_likes = models.IntegerField(default=0)

class Hashtag(models.Model): 
    name = models.CharField(max_length=140)
    tweets = models.ManyToManyField(Tweet)
