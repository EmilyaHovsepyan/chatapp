from django.db import models
from django.contrib.auth.models import User

class messages(models.Model):
    groupname = models.CharField(max_length=30)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(max_length=100, blank=True)
    image = models.ImageField(upload_to='chatphotos', blank=True)

class groupinfo(models.Model):
    groupname = models.CharField(max_length=30)
    members = models.ManyToManyField(User)
    groupimg = models.ImageField(upload_to='grouphotos', blank=True)
    bgname = models.CharField(default='bgdefault')

class userinfo(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=True)
    bio = models.TextField(max_length=100, blank=True)
    photo = models.ImageField(blank=True)
    