from django.urls import include, path
from rest_framework import routers
from . import views #views.py import

from .api import ContentList, ContentDetail, UserList, SignUpView

router = routers.DefaultRouter() #DefaultRouter를 설정
router.register('Item', views.ItemViewSet) #itemviewset 과 item이라는 router 등록

urlpatterns = [
    path('', include(router.urls)),
    path('content_list/', ContentList.as_view(), name="content_list"),
    path('content_list/<int:content_id>/', ContentDetail.as_view(), name="content_detail"),
    path('user_list/', UserList.as_view(), name="user_list"),
    path('signup/',SignUpView.as_view(), name="signup")
]