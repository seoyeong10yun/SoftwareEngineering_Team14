from django.urls import include, path
from rest_framework import routers
from . import views #views.py import

from .api import *

router = routers.DefaultRouter() #DefaultRouter를 설정
router.register('Item', views.ItemViewSet) #itemviewset 과 item이라는 router 등록

urlpatterns = [
    path('', include(router.urls)),
    path('content_list/', ContentListView.as_view(), name="content_list"),
    path('content_list/<int:content_id>/', ContentDetailView.as_view(), name="content_detail"),
    path('user_list/', UserListView.as_view(), name="user_list"),
    path('signup/', SignUpView.as_view(), name="signup"),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('watch_history/', WatchHistoryView.as_view(), name='watch_history'),
    path('add_watch_history/', AddWatchHistoryView.as_view(), name='add_watch_history'),
    path('like_content/', LikeContentView.as_view(), name='like_content'),
    path('dislike_content/', DislikeContentView.as_view(), name='dislike_content'),
]