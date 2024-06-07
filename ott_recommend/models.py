from django.db import models

# Create your models here.
from django.contrib.auth.models import User

#DB구조
class Content(models.Model):
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    release_date = models.DateField()
    rating = models.CharField(max_length=10)  # 부동 소수점이 아닌 문자열로 변경    
    description = models.TextField()
    director = models.CharField(max_length=100, blank=True, null=True)
    cast = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    duration = models.CharField(max_length=50, blank=True, null=True)


    def __str__(self):
        return self.title

class WatchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    watch_date = models.DateTimeField()
    watch_duration = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.content.title}"

# 좋아요한 콘텐츠 테이블
class LikeContent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

# 싫어요한 콘텐츠 테이블
class DislikeContent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)