from django.db import models
from recommand.models import ContentInfo
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    preferred_contents = models.ManyToManyField('recommand.ContentInfo', related_name='preferred_by', blank=True)
    watched_contents = models.ManyToManyField('recommand.ContentInfo', related_name='watched_by', blank=True)
    