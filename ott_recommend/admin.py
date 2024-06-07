from django.contrib import admin

# Register your models here.

from .models import Content, WatchHistory, FavoriteContent, LikeDislike

admin.site.register(Content)
admin.site.register(WatchHistory)
admin.site.register(FavoriteContent)
admin.site.register(LikeDislike)