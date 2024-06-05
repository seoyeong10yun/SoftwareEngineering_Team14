from django.db import models

# Create your models here.
class ContentInfo(models.Model):
    content_id = models.CharField(max_length=255, unique=True, primary_key=True)
    title = models.CharField(max_length=255)
    director = models.CharField(max_length=255)
    description = models.TextField()
    genre = models.CharField(max_length=255)

    def __str__(self):
        return self.title
