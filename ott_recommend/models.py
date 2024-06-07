from django.db import models

# Create your models here.
from django.contrib.auth.models import User

#DB구조
class Content(models.Model):
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    release_date = models.DateField()
    rating = models.FloatField()
    description = models.TextField()

    def __str__(self):
        return self.title

class WatchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    watch_date = models.DateTimeField()
    watch_duration = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.content.title}"

class FavoriteContent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    added_date = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} - {self.content.title}"

class LikeDislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    like = models.BooleanField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} - {self.content.title} - {'Like' if self.like else 'Dislike'}"
