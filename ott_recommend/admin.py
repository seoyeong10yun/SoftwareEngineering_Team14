from django.contrib import admin
from .models import Content, WatchHistory, LikeContent, DislikeContent

admin.site.register(Content)
admin.site.register(WatchHistory)
admin.site.register(LikeContent)
admin.site.register(DislikeContent)

